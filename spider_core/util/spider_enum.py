# -*- coding: utf-8 -*-
# __create:2018/8/21 1:00
# __author:harveyjiang@outlook.com

from enum import Enum, unique


@unique
class SpiderTypeEnum(Enum):
    # 列表页面
    LIST_PAGE = 1
    # 单页面
    SINGE_PAGE = 2
    # Link
    LINK_PAGE = 3
    # API
    API = 4


# print(Method.GET.value) --> get
# print(Method.GET.name) --> GET

