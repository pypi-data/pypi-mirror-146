# -*- coding: utf-8 -*-
# @Time    : 9/19/17 5:16 PM
# @Author  : Tiancheng Zhao

import base64
import numpy as np
from datetime import datetime, timezone
import logging
import os
from soco_trainer_plugin.core.config import EnvVars
import json
import hashlib
import requests
from typing import Sequence, Generator
from rq import get_current_job, Connection
from rq.job import Job
import redis

class Pack(dict):
    def __getattr__(self, name):
        return self[name]

    def clone_dict(self, x):
        for k, v in list(x.items()):
            self[k] = v

    def add(self, **kwargs):
        for k, v in list(kwargs.items()):
            self[k] = v

    def copy(self):
        pack = Pack()
        for k, v in list(self.items()):
            if type(v) is list:
                pack[k] = list(v)
            else:
                pack[k] = v
        return pack


class InvalidUsage(Exception):
    status_code = 400
    """
    The exception contains:
    1. a dictionary containing message (required) and optional dictionary
    2. a status code (HTTP)
    """

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


class Guard(object):
    def __init__(self):
        self.gt_key = ""

    def check(self, api_key):
        """
        :param api_key: a string input
        :return: True if api_key is okay else False
        """
        return api_key.lower() == self.gt_key

    def check_header(self, header):
        if 'authorization' not in header:
            raise InvalidUsage(
                "Missing \'authorization\' api_key in the header ")

        succ = self.check(header['authorization'].lower())
        if not succ:
            raise InvalidUsage("app key authentication failed", 401)
        return succ

    def check_required_fields(self, fields, data):
        #if datetime.now() > datetime(2020,12,15):
        #    raise InvalidUsage("Expire License")
        if data is None:
            raise InvalidUsage("Missing body")

        for f in fields:
            if f not in data:
                raise InvalidUsage('Need to enter \'{}\' as one of the fields in the JSON data'.format(f))


def time_format():
    return "%Y-%m-%dT%H:%M:%S%z"

def current_time():
    return datetime.now(timezone.utc).strftime(time_format())


def decode_float_list(base64_string):
    dfloat32 = np.dtype('>f4')
    bytes = base64.b64decode(base64_string)
    return np.frombuffer(bytes, dtype=dfloat32).tolist()


def encode_array(arr, es_version):
    if es_version == 'default':
        dfloat32 = np.dtype('>f4')
        base64_str = base64.b64encode(np.array(arr).astype(dfloat32)).decode("utf-8")
        return base64_str
    elif es_version == 'builtin':
        return np.array(arr).tolist()
    else:
        raise Exception("Unknown ES version {}".format(es_version))


def prepare_dirs_loggers(config, script="", log_prefix="", session_dir=None):
    logFormatter = logging.Formatter("%(message)s")
    rootLogger = logging.getLogger()
    rootLogger.setLevel(logging.INFO)

    if not os.path.exists(config.log_dir):
        os.makedirs(config.log_dir)
    # since in model_trainer, we want to share the same dock
    if session_dir is None:
        dir_name = "{}-{}".format(current_time(), script) if script else current_time()
        config.session_dir = os.path.join(config.log_dir, dir_name)
        os.mkdir(config.session_dir)
    else:
        config.session_dir = session_dir

    fileHandler = logging.FileHandler(os.path.join(config.session_dir, 'session.log'))
    fileHandler.setLevel(logging.INFO)
    fileHandler.setFormatter(logFormatter)
    rootLogger.addHandler(fileHandler)

    # save config
    param_path = os.path.join(config.session_dir, "{}params.json".format(log_prefix))
    with open(param_path, str('w')) as fp:
        json.dump(config.__dict__, fp, indent=4, sort_keys=True)


def gen_a_key(a):
    return hashlib.md5(json.dumps(a).encode('utf8')).hexdigest()


def save_event():
    requests.post('')


def gen_batch(l: Sequence, n: int = 100) -> Generator[Sequence, None, None]:
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


def current_timestamp(creation_time):
    if type(creation_time) is str:
        d = datetime.strptime(creation_time, time_format())

    if type(creation_time) is datetime:
        d = creation_time

    return int(datetime.timestamp(d)*1000)


def get_queue(name):
    return '{}-{}'.format(EnvVars.redis_queues[0], name)


def is_aborted():
    try:
        logger = logging.getLogger(__name__)
        with Connection(redis.from_url(EnvVars.redis_url)):
            current_job = get_current_job()
            meta = Job.fetch(current_job.get_id()).meta
            if meta.get('is_aborted'):
                return True

            return False
    except Exception as e:
        logger.error(e)
        return False


def get_job_meta(task_id, name, **kwargs):
        meta = {'task_id': task_id,
                'name': name}
        meta.update(kwargs)
        return meta


def dictdiff(d1, d2):
    return dict(set(d2.items()) - set(d1.items()))


if __name__ == "__main__":
    a = {1: 1, 2:2}
    b = {2:2, 3:3}
    print(dictdiff(a, b))
