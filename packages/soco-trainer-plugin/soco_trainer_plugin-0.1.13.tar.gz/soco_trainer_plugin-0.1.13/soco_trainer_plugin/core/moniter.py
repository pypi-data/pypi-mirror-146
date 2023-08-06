from soco_trainer_plugin.core.config import EnvVars, Config, JobState
from soco_trainer_plugin.core.utils import gen_batch
from rq import Connection
from rq.job import Job
from rq import cancel_job
import redis
import logging
import uuid
#from core.agents.mlflow_agent import MLFlow



class Monitor(object):
    def __init__(self, db, redis_url):
        self.logger = logging.getLogger(__name__)
        #self.ml_client = MLFlow()
        self.db = db
        self.redis_url = redis_url

    def _job2dict(self, job):
        response_object = {
            "job_id": job.get_id(),
            "started_at": job.started_at,
            "ended_at": job.ended_at,
            "enqueued_at": job.enqueued_at,
            "job_status": job.get_status(),
            "job_result": job.result,
            "meta": job.meta
        }
        return response_object

    def _fit_old_format(self, op):
        if 'index_progress' in op and 'progress' not in op:
            op['progress'] = op['index_progress']
            keys = list(op['progress'].keys())
            for j_idx, job_meta in enumerate(op.get('job_ids', [])):
                try:
                    op['progress'][keys[j_idx]].update(**job_meta)
                except:
                    pass
            for k in keys:
                if 'job_id' not in op['progress'][k]:
                    op['progress'][k]['job_id'] = 'not_found_{}'.format(uuid.uuid4())

                if op['progress'][k].get('done', 0.0) >= op['progress'][k].get('total', 0.0):
                    op['progress'][k]['status'] = JobState.FINISHED
                else:
                    op['progress'][k]['status'] = JobState.FAILED

            new_progress = {}
            for k, v in op['progress'].items():
                new_progress[v['job_id']] = v

            op['progress'] = new_progress

        if 'progress' in op:
            progress = op['progress']
            if len(progress) > 0 and 'job_id' not in list(progress)[0]:
                keys = list(progress.keys())
                for j_idx, job_meta in enumerate(op.get('job_ids', [])):
                    try:
                        op['progress'][keys[j_idx]].update(**job_meta)
                    except:
                        pass
                new_progress = {}
                for k, v in op['progress'].items():
                    new_progress[v['job_id']] = v
                op['progress'] = new_progress

        op.pop('index_progress', None)
        op.pop('job_ids', None)
        return op
    
    """
    def get_run_info(self, task_id, op_id):
        runs = self.ml_client.get_detail_experiment(task_id)
        if "runs" in runs:
            for y in runs["runs"]:
                for k in y["data"]["params"]:
                    if k["key"] == "op_id" and k["value"] == op_id:
                        return y
        return {}
    """    
    def get_op_status(self, op_id):
        """
        if any of the job is queued, or deferred, then it's that status
        if all finished, then it's finished,
        if any if failed, then it's failed
        :param op_id:
        :return:
        """
        op = self.db.read_op(op_id)
        if not op:
            return {'_id': op_id,
                    'error': 'does not exist',
                    'progress': {},
                    'status': JobState.NOT_FOUND}

        try:
            op = self._fit_old_format(op)
        except Exception as e:
            self.logger.error(e)

        jobs = op.get('progress', {})
        all_done = True
        all_succ = True
        all_started = True
        """
        run = {}
        with Connection(redis.from_url(EnvVars.redis_url)):
            for job_id, job_meta in jobs.items():
                success, job_obj = self.get_job_status(job_id)
                if "meta" in job_obj:
                    run = self.get_run_info(job_obj["meta"]["task_id"], op_id)
                else:
                    run = {}
                if success:
                    job_status = job_obj.get('job_status')
                else:
                    job_status = job_meta.get('status')

                if job_status not in [JobState.FINISHED, None]:
                    all_succ = False

                if job_status not in [JobState.FAILED, JobState.FINISHED, None]:
                    all_done = False

                if job_status in [JobState.DEFERRED, JobState.QUEUED]:
                    all_started = False
        """
        if op.get('is_aborted'):
            op_status = 'aborted'

        else:
            if all_done:
                if all_succ:
                    op_status = JobState.FINISHED
                else:
                    op_status = JobState.FAILED
            else:
                if all_started:
                    op_status = JobState.STARTED
                else:
                    op_status = JobState.QUEUED
        op['status'] = op_status
        op['_id'] = str(op['_id'])
        #op["run"] = run
        return op

    def get_job_status(self, job_id):
        with Connection(redis.from_url(self.redis_url)):
            try:
                job = Job.fetch(job_id)

                if job:
                    job_obj = self._job2dict(job)
                    success = True
                else:
                    raise Exception("Job is None")

            except Exception as e:
                self.logger.error(e)
                job_obj = {'job_id': job_id, 'error': str(e)}
                success = False

            return success, job_obj

    def abort_op(self, op_id):
        """
        """
        current_status = self.get_op_status(op_id)
        if current_status.get('status') in [JobState.FINISHED, JobState.FAILED]:
            raise Exception("Cannot abort because Op=[{}] status=[{}]".format(op_id, current_status.get('status')))

        if current_status.get('is_aborted') or current_status.get('status') == JobState.ABORTED:
            raise Exception('Cannot abort because Op=[{}] is_aborted=True'.format(op_id))

        job_ids = current_status.get('progress', {})
        for job_id, meta in job_ids.items():
            try:
                self.abort_job(job_id)
            except Exception as e:
                self.logger.error(e)

        self.db.write_op_meta(op_id, 'is_aborted', True)

        return True

    def abort_job(self, job_id):
        """
        :param job_id:
        :return:
        """
        with Connection(redis.from_url(self.redis_url)):
            self.logger.info("Cancel job ID {}".format(job_id))
            job = Job.fetch(job_id)
            job_status = job.get_status()

            if job_status in [JobState.QUEUED, JobState.DEFERRED]:
                cancel_job(job_id)

            elif job_status == JobState.STARTED:
                job.meta['is_aborted'] = True
                job.save_meta()

            else:
                self.logger.info("Don't need to abort because Job=[{}] status=[{}]".format(job_id, job_status))

            return job_status

