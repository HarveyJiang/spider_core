MONGODB_CONF = {
    'server'    : 'localhost',
    'port'      : 27017,
    'db'        : 'crawlers',
    'collection': 'news'
}
MYSQL_CONF = {
    'server'  : '127.0.0.1',
    'port'    : 3306,
    'user'    : 'root',
    'password': 'P@ssw0rd',
    'database': 'crawler_setting',
    'charset' : 'latin1'
}
REDIS_CONF = {
    'url' : 'redis://127.0.0.1:6379',
    'host': '127.0.0.1',
    'port': 6379
}
USER_AGENT_CHOICES = [
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:23.0) Gecko/20100101 Firefox/23.0',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.62 Safari/537.36',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; WOW64; Trident/6.0)',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.146 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.146 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64; rv:24.0) Gecko/20140205 Firefox/24.0 Iceweasel/24.3.0',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:28.0) Gecko/20100101 Firefox/28.0',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:28.0) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2',
]

import os

if os.getenv('SCRAPY_FLAG') == 'prod':
    import settings_prod

    MONGODB_CONF = settings_prod.MONGODB_CONF
    REDIS_CONF = settings_prod.REDIS_CONF
