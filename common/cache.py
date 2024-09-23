#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author: Reiner New
email: nbxlc@hotmail.com
"""


from enum import Enum
import importlib
import threading
import requests
from concurrent.futures import ThreadPoolExecutor

from cachetools import cached, LRUCache


from common import py
from .thread import TH_POOL


CACHE = LRUCache(maxsize=100)

class Cache(Enum):

    PYVER = ["common.py", "getPyVer"]


    def getCache(self, name):

        if name in CACHE:
            return CACHE[name]
        print("mark")

    def setCache(self, name, value):
        CACHE[name] = value

    def getCachebyFunc(self, module_name, func_name):

        if func_name in CACHE:
            return CACHE[func_name]

        getVerTh = TH_POOL.submit(getattr(importlib.import_module(module_name, func_name)))
        pyVers = getVerTh.result()
        TH_POOL.shutdown()

        if pyVers:
            CACHE[func_name] = pyVers
            return pyVers

    def get(self):
        if self.name in CACHE:
            return CACHE[self.name]

        getVerTh = TH_POOL.submit(getattr(importlib.import_module(self.value[0]), self.value[1]))
        pyVers = getVerTh.result()

        CACHE[self.name] = pyVers

        return pyVers



@cached(CACHE)
def getPyVer():
    # 获取Python版本列表
    response = requests.get('https://api.github.com/repos/python/cpython/tags')

    # 解析JSON数据
    data = response.json()

    # 获取Python版本列表
    python_versions = [tag['name'] for tag in data if tag['name'].startswith('v')]

    # 打印Python版本列表
    return python_versions