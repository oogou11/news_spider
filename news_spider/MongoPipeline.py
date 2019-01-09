import pymongo

class MongoPipeline(object):
    collection_name = 'scrapy_items'
    collection_message = 'message'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'scrapy_news')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        _id = self.db[self.collection_name].insert(dict(item))
        message_data = {'title': item['title'], 'message_id': str(_id)}
        self.db[self.collection_message].insert(message_data)
        return item
