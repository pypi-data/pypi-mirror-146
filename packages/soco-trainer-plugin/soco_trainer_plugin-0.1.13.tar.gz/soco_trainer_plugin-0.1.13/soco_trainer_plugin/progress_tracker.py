from soco_trainer_plugin.core.database.mongo_api import Database
from soco_trainer_plugin.core.config import JobState
from datetime import datetime
from rq import get_current_job, Connection
import redis
import logging
import time


class ProgressTracker(object):
    def __init__(self, task_id, op_id, job_type, redis_url, mongo_url, debug=False):
        if debug:
            self.debug = True
            return

        with Connection(redis.from_url(redis_url)):
            current_job = get_current_job()
            self.job_id = current_job.get_id()

        self.task_id = task_id
        self.debug = debug
        self.op_id = op_id
        self.job_type = job_type
        self.s_time = time.time()
        self.logger = logging.getLogger(__name__)
        self.op_db = Database(mongo_url)
        self.op_db.write_op_meta(self.op_id, 'progress.{}.type'.format(self.job_id), self.job_type)

    def save_op(self, task_id, name, **kwargs):
        return self.op_db.create_op(task_id, name, **kwargs)

    def append_job_to_op(self, op_id, queue, job_id):
        new_meta = {'progress.{}.job_id'.format(job_id): job_id,
                    'progress.{}.queue'.format(job_id): queue,
                    'progress.{}.status'.format(job_id): JobState.QUEUED,
                    'progress.{}.enqueued_at'.format(job_id): datetime.utcnow()}

        return self.op_db.write_op_metas(op_id, new_meta)

    def start_tracking(self, total):
        if self.debug:
            return
        self.s_time = time.time()
        new_meta = {'progress.{}.started_at'.format(self.job_id): datetime.utcnow(),
                    'progress.{}.total'.format(self.job_id): total,
                    'progress.{}.done'.format(self.job_id): 0,
                    'progress.{}.status'.format(self.job_id): JobState.STARTED}
        return self.op_db.write_op_metas(self.op_id, new_meta)

    def update_done(self, value):
        if self.debug:
            return
        return self.op_db.write_op_meta(self.op_id, 'progress.{}.done'.format(self.job_id), value)

    def finish(self):
        if self.debug:
            return
        took = time.time() - self.s_time
        msg = "Took {} sec to finish {} for task=[{}] op=[{}]".format(took, self.job_id, self.task_id, self.op_id)
        self.logger.info(msg)
        new_meta = {'progress.{}.status'.format(self.job_id): JobState.FINISHED,
                    'progress.{}.res'.format(self.job_id): msg}
        self.op_db.write_op_metas(self.op_id, new_meta)
        return msg

    def error(self, msg):
        if self.debug:
            return
        if type(msg) is not str:
            msg = str(msg)
        self.logger.error("Error: {}".format(msg))
        new_meta = {'progress.{}.status'.format(self.job_id): JobState.FAILED,
                    'progress.{}.error'.format(self.job_id): msg}
        self.op_db.write_op_metas(self.op_id, new_meta)
        return msg


if __name__ == "__main__":
    ProgressTracker.save_op('12', '312', ok=123, lal=2)
