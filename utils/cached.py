import weakref
import redis
from scrapy.utils.project import get_project_settings


class Cached(type):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__cache = weakref.WeakValueDictionary()

    def __call__(self, *args):
        if args in self.__cache:
            return self.__cache[args]
        else:
            obj = super().__call__(*args)
            self.__cache[args] = obj
            return obj


class RedisChannelInit(metaclass=Cached):
    def __init__(self):
        settings = get_project_settings()
        host = settings.get('REDIS_HOST', 'localhost')
        port = settings.get('REDIS_PORT', 6379)
        db = settings.get('PUBLISH_CHANNEL_DB', 1)
        redis_conn = redis.Redis(host=host, port=port, db=db)
        self.name = redis_conn


class PublishMessageToChannel:

    def __init__(self):
        self._redis_conn = RedisChannelInit().name
        self._config = get_project_settings()

    def publish_message(self, message):
        channel_name = self._config.get('PUBLISH_CHANNEL', 'news_spider.job.channel')
        self._redis_conn.pubsub()
        self._redis_conn.publish(channel_name, message)
