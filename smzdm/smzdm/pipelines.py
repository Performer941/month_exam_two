# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient


class SmzdmPipeline(object):
    def process_item(self, item, spider):
        # 导入mangodb
        client = MongoClient("127.0.0.1", 27017)
        collection = client["youhui"]["youhui"]
        collection.insert(item)
