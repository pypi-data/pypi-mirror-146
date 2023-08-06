# -*- coding: utf-8 -*-
# Author: Kyusong Lee
# Date: 09/22/2021

import logging
import json
from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime

import redis
from .utils import InvalidUsage, Guard, get_queue, get_job_meta
from .config import EnvVars, Config
from rq import Queue, Connection
from .agents.k8s_agent import K8S
from .agents.docker_agent import Docker
from .database.mongo_api import Database
from .moniter import Monitor
from .config import JobState
from flask import send_file
import os
import glob2


class Connector(object):
    """
    A connector class that connects a FlowBot to various user interface.
    """

    @staticmethod
    def handle_invalid_usage(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    def __init__(self, debug, trainer, mongo_url, redis_url, param, server_name="trainer"):
        self.app = Flask(__name__)
        self.app.debug = debug
        CORS(self.app)

        # backend interfaces
        self.db = Database(mongo_url)
        self.redis_url = redis_url
        self.guard = Guard()
        self.trainer = trainer
        self.server_name = server_name
        self.logger = logging.getLogger(__name__)
        self.root_dir = os.path.dirname(os.path.realpath(__file__)).replace('soco_trainer_plugin/core', '')
        if EnvVars.mode == "k8s":
            self.cluster_client = K8S()
        else:
            self.cluster_client = Docker()

        self.monitor = Monitor(self.db, redis_url)
        self.param = param

        # add routes to flask App
        self.app.add_url_rule('/v1/trainer/ping', view_func=self.ping, methods=['POST'])

        # add routes to flask App
        self.app.add_url_rule('/v1/trainer/params', view_func=self.params, methods=['GET'])

        # train operations
        self.app.add_url_rule('/v1/trainer/start_train', view_func=self.start_train, methods=['POST'])

        # models
        self.app.add_url_rule('/v1/trainer/models', view_func=self.models, methods=['GET'])
        self.app.add_url_rule('/v1/trainer/download_models/<task_id>', view_func=self.download_model, methods=['GET'])
        self.app.add_url_rule('/v1/trainer/download_models/<task_id>/<model_id>', view_func=self.download_specific_model, methods=['GET'])
        self.app.add_url_rule('/v1/trainer/predict', view_func=self.predict, methods=['GET'])

        # cancel jobs
        self.app.add_url_rule('/v1/trainer/abort_job/<job_id>', view_func=self.abort_job, methods=['GET'])
        self.app.add_url_rule('/v1/trainer/abort_op/<op_id>', view_func=self.abort_op, methods=['GET'])

        # k8s
        self.app.add_url_rule('/v1/trainer/console_logs', view_func=self.console_logs, methods=['POST'])
        self.app.add_url_rule('/v1/trainer/console_logs_by_op_id', view_func=self.console_logs_by_op_id, methods=['POST'])
        self.app.add_url_rule('/v1/trainer/restart_pod', view_func=self.restart_pod, methods=['POST'])

        self.app.register_error_handler(InvalidUsage, self.handle_invalid_usage)

    @classmethod
    def _op2dict(cls, op_id):
        return {'op_id': op_id}

    def params(self):
        return json.load(open(self.param))

    def models(self):
        paths = glob2.glob(f"{self.root_dir}/trained_models/**/*.ckpt")
        data = {}
        output = []
        for path in paths:
            path = path.split("trained_models/")
            if len(path) < 1:
                continue
            path = path[1].split("/")
            if len(path) < 1:
                continue
            task_id, model_id = path
            if not task_id in data:
                data[task_id] = []
            data[task_id].append(model_id)
        for task_id in data:
            output.append({"task_id": task_id, "model_ids":data[task_id]})
        return jsonify({"models":output})

    def download_specific_model(self, task_id, model_id):
        path = f"{self.root_dir}/trained_models/{task_id}/{model_id}"
        return send_file(path, as_attachment=True)

    def download_model(self, task_id):
        path = f"{self.root_dir}/trained_models/{task_id}/best.ckpt"
        return send_file(path, as_attachment=True)

    def predict(self):
        data = request.get_json()
        self.guard.check_required_fields(['task_id','model_id','input','params'], data)
        try:
            output = self.trainer.predict(data["task_id"],data["model_id"], data['params'], data["input"])
        except Exception as e:
            output = {"error":str(e)}
        return jsonify(output)

    def start_train(self):
        """
        :return: make a temp index, process it and only after it's done, replace the current index.
        """
        data = request.get_json()
        print (data)
        self.guard.check_required_fields(['params'], data)
        with Connection(redis.from_url(self.redis_url)):
            params = data['params']
            task_id = data["task_id"]
            task_type = data.get("task_type","span")
            kwargs = data.get('kwargs')
            self.logger.info("start_train task {}".format(data["task_id"]))
            op_id = self.db.create_op(task_id, task_type)

            q = Queue(self.server_name)
            job = q.enqueue(f=self.trainer.start_train,
                            args=(task_id,
                                  op_id,
                                  params,
                                  task_type),
                            kwargs=kwargs,
                            job_timeout=EnvVars.job_ttl,
                            meta=get_job_meta(task_id, task_type))
            job_id = job.get_id()
            new_meta = {'progress.{}.job_id'.format(job_id): job_id,
                        'progress.{}.queue'.format(job_id): q.name,
                        'progress.{}.status'.format(job_id): JobState.QUEUED,
                        'progress.{}.enqueued_at'.format(job_id): datetime.utcnow()}

            self.db.write_op_metas(op_id, new_meta)
            self.logger.info("Job ID=[{}], Op ID=[{}]".format(job.get_id(), op_id))

        return jsonify(self._op2dict(op_id)), 201

    def ping(self):
        """
        :return: bot response
        """
        data = request.get_json()
        return jsonify(data)

    def restart_pod(self):
        data = request.get_json()
        self.guard.check_required_fields(['name'], data)
        results = self.cluster_client.delete_pod(data["name"])
        return 0

    def console_logs(self):
        data = request.get_json()
        self.guard.check_required_fields(['line'], data)
        results = self.cluster_client.get_logs(data["line"])
        return jsonify({"res":results})

    def console_logs_by_op_id(self):
        data = request.get_json()
        self.guard.check_required_fields(['op_id'], data)
        results = self.cluster_client.get_logs_by_op_id(data["op_id"])
        return jsonify({"res": results})

    def abort_job(self, job_id):
        """
        :return:
        """
        #self.guard.check_header(request.headers)
        try:
            kill_status = self.monitor.abort_job(job_id)
            resp = {'code': Config.SUCCESS, 'status': kill_status}
            return jsonify(resp)

        except Exception as e:
            self.logger.error(e)
            raise InvalidUsage("Error: {}".format(str(e)))

    def abort_op(self, op_id):
        #self.guard.check_header(request.headers)
        try:
            result = self.cluster_client.delete_pod_by_op_id(op_id)
            kill_status = self.monitor.abort_op(op_id)
            try:
                if result:
                    resp = {'code': Config.SUCCESS, 'status': kill_status}
                else:
                    resp = {'code': Config.ERROR, 'status': False}
            except:
                resp = {'code': Config.ERROR, 'status': False}

            return jsonify(resp)

        except Exception as e:
            self.logger.error(e)
            raise InvalidUsage("Error: {}".format(str(e)))


if __name__ == '__main__':
    print(get_job_meta('123', 'name', ok=123, abc=332))
