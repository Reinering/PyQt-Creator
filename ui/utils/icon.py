#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author: Reiner
email: nbxlc@hotmail.com
"""


from enum import Enum

from qfluentwidgets import getIconColor, Theme, FluentIconBase, qconfig

from manage import UI_CONFIG


class AppIcon(FluentIconBase, Enum):

    HOME = "home"
    PROJECT = "project"
    DESIGNER = "designer"
    PACK = "pack"
    OTHER = "other"
    CONSOLE = "console"
    DOCUMENT = "document"
    SETTINGS = "settings"
    LOG = "log"

    def path(self, theme=Theme.AUTO):
        theme = qconfig.theme if theme == Theme.AUTO else theme
        return f"{UI_CONFIG['iconPath']}/{theme.value.lower()}/{self.value}.svg"


class AppPic(FluentIconBase, Enum):

    LOAD = "load"


    def path(self, theme=Theme.AUTO):
        return f"{UI_CONFIG['gifPath']}/{self.value}.gif"