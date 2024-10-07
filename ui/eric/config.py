#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author: Reiner New
email: nbxlc@hotmail.com
"""

import os

_pkg_config = "CodeTemplates"


def getConfig():
    '''
    Module function to get a configuration value.

    @param name name of the configuration value    @type str
    @exception AttributeError raised to indicate an invalid config entry
    '''
    try:
        return os.path.join(os.path.dirname(__file__), _pkg_config)
    except KeyError:
        pass

    raise AttributeError(
        'a valid configuration value')
