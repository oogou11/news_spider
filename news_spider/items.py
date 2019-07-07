# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    url = scrapy.Field()
    title = scrapy.Field()
    time = scrapy.Field()
    category = scrapy.Field()
    author = scrapy.Field()
    review = scrapy.Field()
    thumb_url = scrapy.Field()
    content = scrapy.Field()
    source = scrapy.Field()
    create_time = scrapy.Field()
    tags = scrapy.Field()
