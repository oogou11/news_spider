import redis

r = redis.Redis(db=1)

channel = r.pubsub()

channel.subscribe('news_spider.job.channel')
while True:
    data = channel.parse_response()
    mess = channel.get_message()
    print(data, mess)
