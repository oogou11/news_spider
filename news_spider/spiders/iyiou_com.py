import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from news_spider.items import NewsSpiderItem
import lxml.html.clean as clean
import datetime

project_items = {
    'AI': '人工智能',
    'qiche': '汽车',
    'yiliao': '医疗',
    'jiazhuang': '家居',
    'jinrong': '金融',
    'lingshou': '零售',
    'wenchuang': '文创教育',
    'wuliu': '智慧物流',
    'canyin': '生活服务',
    'B2B': 'B2B/企业服务',
    'smartcity': '智慧城市',
    'manufacturing': '新制造',
    'zonghe': '综合'
}

'''
    亿欧
'''
class ScanViewSpider(scrapy.Spider):
    __source = '亿欧网'
    name = "yiou_spider"
    __safe_attrs = set(['src', 'alt', 'href', 'title', 'width', 'height'])
    __kill_tags = ['object', 'iframe']
    allowed_domains = ["iyiou.com"]
    categories = ('AI', 'qiche', 'yiliao', 'jiazhuang', 'jinrong', 'lingshou', 'wenchuang',
                  'wuliu', 'canyin', 'B2B', 'smartcity', 'manufacturing', 'zonghe')

    def start_requests(self):
        for category in self.categories:
            yield scrapy.Request('https://www.iyiou.com/intelligence/insights-{}/'.format(category), self.parse)

    def parse(self, response):
        array_split_url = response.request.url.split('-')
        category = ''
        if len(array_split_url) > 1:
            if '/' in array_split_url[1]:
                category_key = array_split_url[1].split('/')[0]
            else:
                category_key = array_split_url[1]
            category = project_items.get(category_key)
        content_list = response.xpath(".//*[@class='viewpointListWrap contentWrap perspective']/ul/li")
        for content in content_list:
            url = content.xpath(".//a/@href").extract()
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
            item = NewsSpiderItem(url=url, title=title, time=time, author=author,
                                  source=self.__source, category=category, create_time=datetime.datetime.now())
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
        origin_html = body.xpath(".//div[@id='post_description']/p").extract()
        content = list()
        cleaner = clean.Cleaner(safe_attrs_only=True, safe_attrs=self.__safe_attrs, kill_tags=self.__kill_tags)
        for html_string in origin_html:
            cleaned_html = cleaner.clean_html(html_string)
            content.append(cleaned_html)
        item['content'] = content
        yield item

