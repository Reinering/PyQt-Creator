#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author: Reiner New
email: nbxlc@hotmail.com
"""

from concurrent.futures import ThreadPoolExecutor


class ThreadPool():
    def __init__(self, max_workers=5):
        self.max_workers = max_workers

    def init(self):
        self.pool = ThreadPoolExecutor(max_workers=self.max_workers)

    def submit(self, func, *args):
        if len(args) > 0:
            th = self.pool.submit(func, args)
        else:
            th = self.pool.submit(func)
        return th.result()

    def shutdown(self):
        self.pool.shutdown()



TH_POOL = ThreadPool()
TH_POOL.init()