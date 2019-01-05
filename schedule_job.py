import logging
from apscheduler.schedulers.blocking import BlockingScheduler


scheduler = BlockingScheduler()
logging.basicConfig()
logging.getLogger('apscheduler.executors.default').setLevel(logging.DEBUG)
scheduler._logger = logging


class HandleJob(object):

    @classmethod
    def stop_job(cls, job_id):
        scheduler.remove_job(job_id)

    @classmethod
    def pausing_job(cls, job_id):
        scheduler.pause_job(job_id)

    @classmethod
    def resuming_job(cls, job_id):
        scheduler.pause_job(job_id)

    @classmethod
    def get_jobs(cls):
        data = scheduler.get_jobs()
        return data

    @classmethod
    def get_job_logger(cls, job_id):
        pass
