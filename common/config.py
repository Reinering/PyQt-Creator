#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author: Reiner New
email: nbxlc@hotmail.com
"""


import simplejson as json


def write_config(settingFile, setting):

    with open(settingFile, 'w') as f:
        tmp = ''
        if isinstance(setting, dict):
            tmp = json.dumps(setting, indent=4)
        else:
            tmp = setting
        f.write(tmp)
