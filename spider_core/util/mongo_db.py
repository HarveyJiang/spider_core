# -*- coding: utf-8 -*-
# __create:2017/9/15 23:16


import pymongo
from scrapy.conf import settings


def init_mongodb():
    mongodb_conf = settings.get('MONGODB_CONF')
    server = mongodb_conf.get('server')
    port = mongodb_conf.get('port')
    mongodb_db = mongodb_conf.get('db')
    collection = mongodb_conf.get('collection')
    client = pymongo.MongoClient(server, port)
    db = client[mongodb_db][collection]
    # print client.server_info()
    return db
