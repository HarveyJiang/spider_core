# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


# class SpiderCoreItem(scrapy.Item):
#     # define the fields for your item here like:
#     # name = scrapy.Field()
#     pass
#
# import scrapy


class SpiderCoreItem(scrapy.Item):
    # ... other item fields ...
    _id = scrapy.Field()

    def __setitem__(self, key, value):
        if key not in self.fields:
            self.fields[key] = scrapy.Field()
        super(SpiderCoreItem, self).__setitem__(key, value)
