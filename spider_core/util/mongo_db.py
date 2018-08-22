# -*- coding: utf-8 -*-
# __create:2017/9/15 23:16

import pymongo
from scrapy.conf import settings

from spider_core.util.common import singleton


@singleton
class MongodHelper(object):
    def __init__(self, crawler=None):
        self.init_mongodb(crawler)

    def init_mongodb(self, crawler):
        s = crawler.settings if crawler else settings
        mongodb_conf = s.get('MONGODB_CONF')
        server = mongodb_conf.get('server')
        port = mongodb_conf.get('port')
        mongodb_db = mongodb_conf.get('db')
        collection = mongodb_conf.get('collection')
        self._client = pymongo.MongoClient(server, port)
        self.db = self._client.get_database(mongodb_db)

    def close(self):
        try:
            self._client.close()
        except:
            pass

    def insert_documents(self, documents, collection_name='default'):
        if isinstance(documents, list):
            print('collections.Iterable')
            self.db.get_collection(collection_name).insert_many(documents)
        elif isinstance(documents, dict):
            print('dict.dict')
            self.db.get_collection(collection_name).insert(documents)
        else:
            raise Exception("not support type insert mongo")
