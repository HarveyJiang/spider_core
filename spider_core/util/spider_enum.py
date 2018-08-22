# -*- coding: utf-8 -*-
# __create:2018/8/21 1:00
# __author:harveyjiang@outlook.com

from enum import Enum, unique


@unique
class SpiderTypeEnum(Enum):
    # 列表页面
    LIST_PAGE = 0
    # 单页面
    SINGE_PAGE = 1
    # Link
    LINK_PAGE = 2
    # API
    API = 3


# print(Method.GET.value) --> get
# print(Method.GET.name) --> GET

