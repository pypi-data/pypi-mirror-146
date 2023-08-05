import logging
import pytz

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from wintersweet.asyncs.task.interfaces import TaskInterface
from wintersweet.utils.base import Utils

TIMEZONE = pytz.timezone(Utils.os.getenv('_TIMEZONE', r'Asia/Shanghai'))


logging.getLogger(r'apscheduler').setLevel(logging.WARNING)


class BaseAsyncIOScheduler(AsyncIOScheduler):
    _instance = None

    def __init__(self):

        super(BaseAsyncIOScheduler, self).__init__(
            job_defaults={
                r'coalesce': False,
                r'max_instances': 1,
                r'misfire_grace_time': 10
            },
            timezone=TIMEZONE
        )

        self.start()

    def __new__(cls, *args, **kwargs):
        if cls._instance:
            return cls._instance

        return super().__new__(cls, *args, **kwargs)


class BaseTask(TaskInterface):

    def __init__(self, func, alone, *args, **kwargs):
        super(BaseTask, self).__init__()
        self._alone = alone
        if alone:
            self._scheduler = AsyncIOScheduler(
                job_defaults={
                    r'coalesce': False,
                    r'max_instances': 1,
                    r'misfire_grace_time': 10
                },
                timezone=TIMEZONE
            )
            self._scheduler.start()
        else:
            self._scheduler = BaseAsyncIOScheduler()
        self._func = Utils.package_task(func, *args, **kwargs)
        self._job = None

    @property
    def scheduler(self):
        return self._scheduler

    def start(self):
        self._job = self._scheduler.add_job(**self._job_args())
        self._running = True
        return self._job

    def stop(self):
        assert self._job is not None, f'{self.__class__.__name__} has no start'
        self._scheduler.remove_job(self._job.id)
        self._job = None
        self._running = False
        return True

    def _job_args(self):

        raise InterruptedError

    def __del__(self):
        if self._alone:
            _scheduler, self._scheduler = self._scheduler, None
            if _scheduler.running:
                _scheduler.shutdown()


class IntervalTask(BaseTask):
    """间隔触发任务"""

    def __init__(self, interval: int, func, *args, alone=False, **kwargs):

        super(IntervalTask, self).__init__(func, alone, *args, **kwargs)
        self._interval = interval

    def _job_args(self):
        return {
            'func': self._func,
            'trigger': r'interval',
            'seconds': self._interval
        }


class CrontabTask(BaseTask):
    """定时触发任务"""
    def __init__(self, crontab, func, *args, alone=False, **kwargs):
        super(CrontabTask, self).__init__(func, alone, *args, **kwargs)
        self._crontab = crontab

    def _job_args(self):
        return {
            'func': self._func,
            'trigger': CronTrigger.from_crontab(self._crontab, TIMEZONE),
        }
