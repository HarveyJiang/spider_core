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


@unique
class SpiderStatusEnum(Enum):
    NEW = 0
    WATING = 1
    RUNNING = 2
    STOP = 3
    FINISHED = 4
    EXCEPTION = 5

# print(Method.GET.value) --> get
# print(Method.GET.name) --> GET
