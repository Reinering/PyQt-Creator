#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author: Reiner New
email: nbxlc@hotmail.com
"""


from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QColor
from qfluentwidgets import InfoBar, InfoBarPosition, MessageBoxBase, SubtitleLabel, LineEdit, CaptionLabel

# from qfluentexpand.components.line.editor import Line



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
    def error(title, content, parent, isClosable=True, duration=30000, position=InfoBarPosition.BOTTOM):
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


class MessageBox(MessageBoxBase):

    def __init__(self, title, placeholderText=None, warnText=None, parent=None):
        super().__init__(parent)
        titleLabel = SubtitleLabel(title, self)
        self.line = LineEdit(self)
        self.line.setReadOnly(False)

        if placeholderText:
            self.line.setPlaceholderText(placeholderText)
        self.line.setClearButtonEnabled(True)

        self.warning = CaptionLabel(warnText)
        self.warning.setTextColor("#cf1010", QColor(255, 28, 32))

        self.viewLayout.addWidget(titleLabel)
        self.viewLayout.addWidget(self.line)
        self.viewLayout.addWidget(self.warning)
        self.warning.hide()

        self.widget.setMinimumWidth(350)

    def validate(self):
        """ 重写验证表单数据的方法 """
        isValid = QUrl(self.line.text()).isValid()
        self.warning.setHidden(isValid)
        return isValid

    def setText(self, text):
        self.line.setText(text)

    def text(self):
        return self.line.text()

