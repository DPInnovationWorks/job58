# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from pymongo.errors import DuplicateKeyError

class MongoDBPipeline(object):
    def __init__(self):
        client = pymongo.MongoClient()
        db = client["Job58"]
        self.collection = db['Job']

    def process_item(self, item, spider):
        self.insert_item(self.collection, item)
        return item

    @staticmethod
    def insert_item(collection, item):
        try:
            collection.insert(dict(item))
        except DuplicateKeyError:
            """
            说明有重复数据
            """
            pass

