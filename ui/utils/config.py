#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author: Reiner
email: nbxlc@hotmail.com
"""

from common.config import Config
from manage import SETTINGS



def saveConfig():
    config = Config()
    config.write(SETTINGS)

