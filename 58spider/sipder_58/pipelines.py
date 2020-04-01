# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

class Sipder58Pipeline(object):
    def process_item(self, item, spider):
        return item

class ToMongoPipeline(object):
    def __init__(self):
        # 创建MONGODB数据库链接
        client = pymongo.MongoClient(host='127.0.0.1', port=27017)
        # 指定数据库
        mydb = client['job58']
        # 存放数据的数据库表名
        self.post = mydb['job58']
