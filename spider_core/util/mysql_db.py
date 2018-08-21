# -*- coding: utf-8 -*-
# __create:2018/8/15 23:32
# __author:harveyjiang@outlook.com
import pymysql
from scrapy.conf import settings

from spider_core.util.common import singleton


@singleton
class MySqlHelper(object):
    # def __new__(cls):
    #     # 关键在于这，每一次实例化的时候，我们都只会返回这同一个instance对象
    #     if not hasattr(cls, 'instance'):
    #         cls.instance = super().__new__(cls)
    #     return cls.instance
    def __init__(self, crawler=None):
        self._client = self.init_mysqldb(crawler)

    def init_mysqldb(self, crawler):
        s = crawler.settings if crawler else settings
        config = s.get('MYSQL_CONF')
        server = config.get('server')
        port = config.get('port')
        user = config.get('user')
        password = config.get('password')
        database = config.get('database')
        charset = config.get('charset') or 'latin1'
        return pymysql.connect(host=server,
                               port=port,
                               user=user,
                               password=password,
                               database=database,
                               charset=charset, cursorclass=pymysql.cursors.DictCursor)

    def get_setting_by_id(self, id):
        cursor = self._client.cursor()
        # cursor.execute('select * from spider where id=%(id)s', {'id': id})
        cursor.execute('select * from spider where id=%s', id)
        r = cursor.fetchone()
        cursor.close()
        return r

    def get_urls_by_id(self, spider_id):
        cursor = self._client.cursor()
        cursor.execute('SELECT * FROM crawler_setting.spider_start_urls where SpiderId=%s and length(Url)>0;',
                       spider_id)
        for row in cursor:
            yield row
        cursor.close()

    def close(self):
        try:
            self._client.close()
        except:
            pass
# mysql = MySqlHelper()
# mysql.get_setting_by_id('2')
# def connect_wxremit_db():
#     con = init_mysqldb()
#     cur = con.cursor()
#     cur.execute('select * from spider')
#     rows = cur.fetchall()
#     print(rows)
#     cur.close()
#     con.close()
#
#
# connect_wxremit_db()
