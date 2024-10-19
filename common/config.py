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


def diff_config(setting, defaultSetting):
    if isinstance(defaultSetting, dict):
        for key, value in defaultSetting.items():
            if key in setting:
                if isinstance(value, dict):
                    diff_config(setting[key], value)
                else:
                    defaultSetting[key] = setting[key]

