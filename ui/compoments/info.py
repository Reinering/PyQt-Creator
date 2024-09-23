#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author: Reiner New
email: nbxlc@hotmail.com
"""


from PySide6.QtCore import Qt
from qfluentwidgets import InfoBar, InfoBarPosition



class Message():
    def __init__(self):
        pass

    @staticmethod
    def info(title, content, parent, isClosable=True, duration=10000, position=InfoBarPosition.BOTTOM):
        InfoBar.info(
            title=title,
            content=content,
            orient=Qt.Orientation.Vertical,  # 内容太长时可使用垂直布局
            isClosable=isClosable,
            position=position,
            duration=duration,
            parent=parent
        )

    @staticmethod
    def success(title, content, parent, isClosable=True, duration=10000, position=InfoBarPosition.BOTTOM):
        InfoBar.success(
            title=title,
            content=content,
            orient=Qt.Orientation.Vertical,  # 内容太长时可使用垂直布局
            isClosable=isClosable,
            position=position,
            duration=duration,
            parent=parent
        )

    @staticmethod
    def error(title, content, parent, isClosable=True, duration=10000, position=InfoBarPosition.BOTTOM):
        InfoBar.error(
            title=title,
            content=content,
            orient=Qt.Orientation.Vertical,  # 内容太长时可使用垂直布局
            isClosable=isClosable,
            position=position,
            duration=duration,
            parent=parent
        )

    @staticmethod
    def warning(title, content, parent, isClosable=True, duration=10000, position=InfoBarPosition.BOTTOM):
        InfoBar.warning(
            title=title,
            content=content,
            orient=Qt.Orientation.Vertical,  # 内容太长时可使用垂直布局
            isClosable=isClosable,
            position=position,
            duration=duration,
            parent=parent
        )

