# -*- coding: utf-8 -*-
# __create:2018/8/20 23:08
# __author:harveyjiang@outlook.com

def singleton(cls):
    instances = {}

    def wrapper(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return wrapper
