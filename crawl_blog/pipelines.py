# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from pymongo import MongoClient
from scrapy.conf import settings
from scrapy import log

class MongoDBPipeline(object):
    def __init__(self):
        connection = MongoClient(settings.get('MONGODB_URI'))
        db = connection[settings['MONGODB_DATABASE']]
        # db.authenticate(settings['MONGODB_USERNAME'], settings['MONGODB_PASSWORD'])
        self.collection = db[settings['CRAWLER_COLLECTION']]

    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        log.msg("Item wrote to MongoDB database {}, collection {}, at host {}".format(
            settings['MONGODB_DATABASE'],
            settings['CRAWLER_COLLECTION'],
            settings['MONGODB_URI']),level=log.DEBUG, spider=spider)
        return item
