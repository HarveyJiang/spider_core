# -*- coding: utf-8 -*-
import json
import sys
import threading

from scrapy import Request, signals
from scrapy.spiders import CrawlSpider

from spider_core.util.login import login_handler
from spider_core.util.mongo_db import MongodHelper
from spider_core.util.mysql_db import MySqlHelper
from spider_core.util.spider_enum import SpiderStatusEnum, SpiderTypeEnum


class BaseSpider(CrawlSpider):
    name = 'base'
    # allowed_domains = ['example.com']
    # start_urls = ['http://baidu.com']
    mysql_helper = MySqlHelper()
    mongod_helper = MongodHelper()
    print('BaseSpider', id(mysql_helper))

    def __init__(self, **kwargs):

        self.init_rules()
        super().__init__(**kwargs)
        self.is_list_page = self.spider_settings.get('SpiderType') == SpiderTypeEnum.LIST_PAGE.value
        print('islis', self.is_list_page, type(self.spider_settings.get('SpiderType')))
        self.default_kwargs = {
            'method'     : 'GET',
            'callback'   : self.parse_list if self.is_list_page else self.parse,
            'meta'       : {
                'cookiejar': self.spider_id,
            },
            'encoding'   : 'utf-8',
            'dont_filter': False,
            'errback'    : self.spider_error,
            'cookies'    : None
        }
        self.check_manual_stop()

    def init_rules(self):
        setting = self.spider_settings
        if setting.get('SpiderType') == SpiderTypeEnum.LINK_PAGE.value:
            # rules = (
            #     Rule(LinkExtractor(allow=('category\.php',), deny=('subsection\.php',))),
            #     Rule(LinkExtractor(allow=('item\.php',)), callback='parse_item'),
            # )
            self.rules = ()

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super().from_crawler(crawler, *args, **kwargs)
        spider.stats = crawler.stats
        crawler.signals.connect(spider.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider

    @classmethod
    def update_settings(cls, settings):
        argv3 = sys.argv[3].split('=')[-1]
        # assert isinstance(argv3, int), 'spider_id type error , only int type.'
        spider_id = int(argv3)
        # if spider_id <= 0:
        #     raise Exception("spider_id arg invaild.")
        # cls.custom_settings = {'ROBOTSTXT_OBEY': False}
        # spider_id = settings.get('spider_id')
        print('spider_id', spider_id)
        setting = cls.mysql_helper.get_setting_by_id(spider_id)
        cls.spider_id = spider_id
        cls.spider_name = 'spider_{}'.format(setting.get('Name'))
        cls.spider_settings = setting
        cls.allowed_domains = setting.get('Domains') if setting.get('AllowedDomain') else []

        cls.custom_settings = setting.get('ScrapySettings') or {}
        # cls.custom_settings.update({'COOKIES_ENABLED': False})
        # cls.custom_settings.update({'DOWNLOADER_MIDDLEWARES': 'mySpider.middlewares.ProxiesMiddleware'})
        super().update_settings(settings)

    def start_requests(self):
        setting = self.spider_settings
        kwargs = self.default_kwargs.copy()
        if setting.get('IsLogin'):
            login_url, login_args = setting.get('LoginUrl'), setting.get('LoginArgs')
            kwargs['cookies'] = login_handler(login_url, login_args)
        urls = self.mysql_helper.get_urls_by_id(self.spider_id)
        for url in urls:
            kwargs['encoding'] = url.get('RequestEncoding') or kwargs.get('encoding')
            kwargs['method'] = url.get('RequestMethod') or kwargs.get('method')
            info = {
                'list_fields'  : json.loads(url.get('ListFields')),
                'detail_fields': json.loads(url.get('DetailFields')),
                'list_info'    : json.loads(url.get('ListInfo')),
                'page_info'    : json.loads(url.get('PageInfo'))
            }
            kwargs.get('meta').update(info)
            yield self.builder_request(url.get('Url'), **kwargs)
        # yield Request('http://www.baidu.com', dont_filter=True)

    def spider_opened(self, spider):
        self.mysql_helper.update_spider_status(SpiderStatusEnum.RUNNING.value, self.spider_id)
        print('spider_opened spider.name', spider.name)

    def spider_closed(self, spider):
        # self.mysql_helper.close()
        self.mongod_helper.close()
        # print(' self.crawler', dir(self.crawler.spiders))
        # print(' self.crawler.engine', dir(self.crawler.engine))
        print('spider_closed spider.name', spider.name, self.name)

    def parse(self, response):
        meta = response.meta
        list_item = meta.get('list_item')
        detail_fields = meta.get('detail_fields')
        for k, v in detail_fields.items():
            if k in ['image_urls', 'file_urls']:
                list_item[k] = response.xpath(v).extract()
            else:
                list_item[k] = ''.join(response.xpath(v).extract()).strip()
        list_item['response_url'] = response.url
        yield list_item

    def parse_list(self, response):
        meta = response.meta.copy()
        list_info = meta.pop('list_info')
        list_fields = meta.pop('list_fields')

        list = response.xpath(list_info.get('listXpath'))

        # response.xpath('//parent').xpath('string(.//a)')  “.” 表示相对上个xpath
        # response.xpath('//parent//a//text()')
        for item in list:
            list_item = {}
            detail_meta = meta
            detail_url = item.xpath(list_info.get('detailXpath')).extract_first()
            if detail_url:
                for k, v in list_fields.items():
                    list_item[k] = ''.join(item.xpath(v).extract()).strip()
                detail_meta.update({'list_item': list_item})
                yield Request(detail_url, meta=detail_meta, dont_filter=True)
        yield self.find_next_page(response)

    def find_next_page(self, response):
        meta = response.meta.copy()
        next_page_xpath = meta.get('page_info').get('nextPageXpath')
        # 页码下一页xpath
        next_page = response.xpath(next_page_xpath).extract_first()
        print('page_count', int(meta.get('page_info').get('page_count', 1)))
        if next_page:
            # 最多爬取多少页码
            max_count = int(meta.get('page_info').get('maxPageCount'))
            if max_count:
                page_count = int(meta.get('page_info').get('page_count', 1))
                if page_count < max_count:
                    meta.get('page_info')['page_count'] = page_count + 1
                    return response.follow(next_page, meta=meta, callback=self.parse_list)
            else:
                return response.follow(next_page, meta=meta, callback=self.parse_list)

    def spider_error(self, failure):
        pass

    def builder_request(self, url, **kwargs):
        print('builder_request kwargs:', kwargs)
        return Request(url, **kwargs)
        # request = Request(url, method='POST',
        #                   body=json.dumps({}),
        #                   headers={'Content-Type': 'application/json'})

    def check_manual_stop(self):
        """
        检测是否触发了停止爬虫
        :return:
        """
        threading.Timer(1, self.manual_stop).start()
        # self.timer = threading.Timer(1, self.manual_stop)
        # self.timer.start()
        # self.timer.cancel()

    def manual_stop(self):
        engine_running = self.crawler.engine.running
        crawler_crawling = self.crawler.crawling
        if engine_running or crawler_crawling:
            status = self.mysql_helper.get_spider_status(self.spider_id)
            if status == SpiderStatusEnum.STOP.value:
                self.crawler.engine.close_spider(self, reason='manual stop')
                # self.mysql_helper.update_spider_status(SpiderStatusEnum.STOP.value, self.spider_id)
            else:
                threading.Timer(1, self.check_manual_stop).start()
