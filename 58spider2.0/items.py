# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Tch58Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    job = scrapy.Field()
    company = scrapy.Field()
    salery = scrapy.Field()
    message_1 = scrapy.Field()
    message_2 = scrapy.Field()
    message_job1 = scrapy.Field()
    message_job2 = scrapy.Field()
    contact = scrapy.Field()
    message_company = scrapy.Field()
    place = scrapy.Field()
    message_company2_1 = scrapy.Field()
    message_company2_2 = scrapy.Field()
    message_company2_3 = scrapy.Field()
