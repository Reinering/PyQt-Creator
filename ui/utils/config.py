#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author: Reiner
email: nbxlc@hotmail.com
"""


import os
import simplejson as json
from manage import ROOT_PATH, SettingPath, SettingFile, CURRENT_SETTINGS


def write_config():

    with open(os.path.join(ROOT_PATH, SettingPath, SettingFile), 'w') as f:
        setting = ''
        if isinstance(CURRENT_SETTINGS, dict):
            setting = json.dumps(CURRENT_SETTINGS, indent=4)
        elif isinstance(CURRENT_SETTINGS, str):
            setting = CURRENT_SETTINGS
        else:
            return

        f.write(setting)
