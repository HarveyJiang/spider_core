# -*- coding: utf-8 -*-
# __create:2018/8/23 21:46
# __author:harveyjiang@outlook.com

"""
爬虫主入口
"""
import subprocess
import time
from datetime import datetime

from spider_core.util.mysql_db import MySqlHelper

# process = CrawlerProcess({
#     'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
# })

# 可以添加多个spider
# process.crawl(SinaNewsSpider)
# process.crawl(News163Spider)
# process.crawl(SohuNewsSpider)
mysql = MySqlHelper()


# print('process:', id(mysql))
# process.crawl('base')
# # 启动爬虫，会阻塞，直到爬取完成
# print('start...')
# process.start()
# print('over..')


def check_waiting_status():
    cursor = mysql.get_wating_spiders()
    for row in cursor:
        #     settings = get_project_settings()
        #     settings.update({'spider_id': row.get('Id')})
        #     process = CrawlerProcess(settings=settings)
        #     process.crawl('base')
        #     process.start()
        #     # multiprocessing
        subprocess.Popen("scrapy crawl base -a spider={0}".format(row.get('Id')))


if __name__ == '__main__':
    while 1:
        check_waiting_status()
        print('loop:', datetime.now())
        time.sleep(5)
