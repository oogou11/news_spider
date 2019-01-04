import scrapy
import logging
from scrapy import Selector
from scrapy.crawler import CrawlerProcess
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from news_spider.items import NewsSpiderItem


'''
    亿欧
'''
class ScanViewSpider(scrapy.Spider):
    __source = '亿欧网'
    name = "yiou_spider"
    allowed_domains = ["iyiou.com"]
    start_urls = [
      "https://www.iyiou.com/intelligence/insights/"
    ]
    # \bintelligence\S*?html\b
    rules = (
        Rule(LinkExtractor(allow=('intelligence/insights-.*/.*',)), callback='parse', follow=True),
    )

    def parse(self, response):
        content_list = response.xpath(".//*[@class='viewpointListWrap contentWrap perspective']/ul/li")
        for content in content_list:
            url = content.xpath(".//a/@href").extract()
            logging.info('....new..url', url)
            if len(url) > 0:
                url = url[0]
            title = content.xpath(".//a/p[@class='perspectiveTitle']/text()").extract()
            if len(title) > 0:
                title = title[0]
            time = content.xpath(".//a/p[@class='researchInfo']/span[@class='time']/text()").extract()
            if len(time) > 0:
                time = time[0]
            author = content.xpath(".//a/p[@class='researchInfo']/span[@class='author']/text()").extract()
            if len(author) > 0:
                author = author[0]
            item = NewsSpiderItem(url=url, title=title, time=time, author=author, source=self.__source)
            request = scrapy.Request(url=url, callback=self.parse_body)
            request.meta['item'] = item  # 将item暂存
            yield request
        next_page = response.xpath(".//*[@id='page']/ul/li[@class='active']/following-sibling::*[1]/a/@href").extract()
        if len(next_page) > 0:
            yield scrapy.Request(url=next_page[0], callback=self.parse)

    def parse_body(self, response):
        item = response.meta['item']
        body = response.xpath(".//*[@class='viewpointWrap']")
        review = body.xpath(".//div[@id='post_brief']/text()").extract()
        if len(review) > 0:
            item['review'] = review[0]
        thumb_url = body.xpath(".//div[@id='post_thumbnail']/img/@src").extract()
        if len(thumb_url) > 0:
            item['thumb_url'] = thumb_url[0]
        item['content'] = body.xpath(".//div[@id='post_description']/p").extract()
        yield item

