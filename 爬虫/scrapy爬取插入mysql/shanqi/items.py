# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ShanqiItem(scrapy.Item):
    # define the fields for your item here like:
    nianling = scrapy.Field()
    xingbie = scrapy.Field()
    title = scrapy.Field()
    zhenduan = scrapy.Field()
