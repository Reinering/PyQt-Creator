#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author: Reiner New
email: nbxlc@hotmail.com
"""


from enum import Enum

from qfluentwidgets import StyleSheetBase, Theme, isDarkTheme, qconfig
from manage import UI_CONFIG


class StyleSheet(StyleSheetBase, Enum):
    """ Style sheet  """

    MAIN = "MAIN"
    PROJECT = "PROJECT"
    DESIGNER = "DESIGNER"
    PACK = "PACK"
    OTHER = "OTHER"
    CONSOLE = "CONSOLE"
    SETTING = "SETTING"

    def path(self, theme=Theme.AUTO):
        theme = qconfig.theme if theme == Theme.AUTO else theme
        return f"{UI_CONFIG['stylesheetPath']}/{theme.value.lower()}/{self.value.lower()}.qss"