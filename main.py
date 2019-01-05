import logging
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from schedule_job import scheduler


process = CrawlerProcess(get_project_settings())
process.crawl('yiou_spider')


@scheduler.scheduled_job('cron', id='yi_ou_job', hour=12, minute=10)
def spider_job():
    process.start()


scheduler.start()
