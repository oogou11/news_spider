from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from news_spider.spiders.iyiou_com import ScanViewSpider

if __name__=='__main__':
    process = CrawlerProcess(get_project_settings())
    process.crawl('yiou_spider')
    process.start()
