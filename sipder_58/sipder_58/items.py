# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Sipder58Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    place = scrapy.Field()  # 工作地点
    job = scrapy.Field()  # 职位
    company = scrapy.Field()  # 公司名称
    salary = scrapy.Field()  # 薪资
    contact = scrapy.Field()  # 联系方式
    job_information = scrapy.Field()  # 职位信息
    requirement = scrapy.Field()  # 招聘要点
    welfare = scrapy.Field()  # 福利
    company_category = scrapy.Field()  # 公司性质
    company_member = scrapy.Field()  # 公司人数
    company_direction = scrapy.Field()  # 公司类别
    other = scrapy.Field() # 其他
    link = scrapy.Field()
    keyword = scrapy.Field()
    time = scrapy.Field()
