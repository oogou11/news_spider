import redis
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from news_spider.spiders.iyiou_com import ScanViewSpider
from apscheduler.schedulers.blocking import BlockingScheduler


sched = BlockingScheduler()

@sched.scheduled_job('cron', id='yi_ou_job', hour=9, minute=40)
def spider_job():
    process = CrawlerProcess(get_project_settings())
    process.crawl('yiou_spider')
    process.start()


sched.start()
