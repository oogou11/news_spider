import logging
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from news_spider.spiders.iyiou_com import ScanViewSpider
from apscheduler.schedulers.blocking import BlockingScheduler


process = CrawlerProcess(get_project_settings())
process.crawl('yiou_spider')
sched = BlockingScheduler()

@sched.scheduled_job('cron', id='yi_ou_job', hour=20, minute=33)
def spider_job():
    logging.info('....waiting......')
    process.start()

sched.start()
