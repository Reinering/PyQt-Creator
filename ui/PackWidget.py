#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author: Reiner New
email: nbxlc@hotmail.com
Module implementing PackWidget.
"""


from PySide6.QtCore import Slot, QRect, Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget, QGridLayout, QHBoxLayout, QVBoxLayout, QSpacerItem, QSizePolicy

from qfluentwidgets import (
    ExpandGroupSettingCard,
    PrimaryPushButton,
    BodyLabel, TitleLabel, CaptionLabel,
    ScrollArea,
    CardWidget, IconWidget, ComboBox
)
from qfluentwidgets.common.icon import isDarkTheme, FluentIconBase, FluentIconBase as FIF, FluentIcon

from qfluentexpand.components.card.settingcard import SettingGroupCard
from qfluentexpand.components.line.selector import FilePathSelector

from .Ui_PackWidget import Ui_Form
from .utils.stylesheets import StyleSheet


class PackWidget(QWidget, Ui_Form):
    """
    Class documentation goes here.
    """

    def __init__(self, parent=None):
        """
        Constructor

        @param parent reference to the parent widget (defaults to None)
        @type QWidget (optional)
        """
        super().__init__(parent)
        self.setupUi(self)
        self.setObjectName("pack")
        StyleSheet.PACK.apply(self)

        self.gridLayout1 = QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout1.setObjectName(u"gridLayout")
        self.gridLayout1.setContentsMargins(50, -1, 50, -1)
        self.gridLayout1.setSpacing(30)
        self.gridLayout1.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.initTitle()
        self.initWidget()


    def initTitle(self):
        self.titleCard = CardWidget(self)
        self.titleCard.setMinimumHeight(200)
        self.gridLayout1.addWidget(self.titleCard, 0, 0, 1, 1)
        # self.ScrollArea.setViewportMargins(0, self.titleCard.height(), 0, 0)
        self.ScrollArea.setWidgetResizable(True)

        titleLabel = TitleLabel("Pack", self)
        subtitleLabel = CaptionLabel("pyinstaller / Nuitka", self)

        hBoxLayout = QHBoxLayout(self.titleCard)
        hBoxLayout.setSpacing(0)
        hBoxLayout.setContentsMargins(36, 22, 36, 12)

        hBoxLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        vBoxLayout = QVBoxLayout(self.titleCard)
        vBoxLayout.setSpacing(0)
        vBoxLayout.setContentsMargins(36, 22, 36, 12)
        vBoxLayout.addWidget(titleLabel)
        vBoxLayout.addSpacing(4)
        vBoxLayout.addWidget(subtitleLabel)
        vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        hBoxLayout.addLayout(vBoxLayout)

        openBtn = PrimaryPushButton(self.titleCard)
        openBtn.setText("打开")
        openBtn.setMinimumWidth(100)
        openBtn.setMinimumHeight(40)
        hBoxLayout.addWidget(openBtn, 0, Qt.AlignmentFlag.AlignRight)



    def initWidget(self):
        self.envcard = SettingGroupCard(FluentIcon.SPEED_OFF, "环境设置", "",
                         self.scrollAreaWidgetContents)
        widget = QWidget(self.envcard)
        iconWidget = IconWidget(FluentIcon.SPEED_OFF)
        titleLabel = BodyLabel("模式", self.envcard)
        items = ["跟随项目", "跟随全局", "独立模式"]
        comboBox = ComboBox(self.envcard)
        comboBox.addItems(items)
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(30, 5, 30, 5)
        layout.addWidget(iconWidget)
        layout.addWidget(titleLabel)
        layout.addStretch(1)
        layout.addWidget(comboBox)
        self.envcard.addWidget(widget)

        widget = QWidget(self.envcard)
        envLabel = BodyLabel("Python 环境")
        envButton = FilePathSelector(self.envcard)
        envButton.setText("选择")
        envButton.setFileTypes("python.exe")
        envButton.setFixedWidth(200)
        envButton.setEnabled(False)
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(30, 5, 30, 5)
        layout.addWidget(envLabel)
        layout.addStretch(1)
        layout.addWidget(envButton)
        self.envcard.addWidget(widget)

        # self.hBoxLayout = QHBoxLayout(self.envcard)
        # iconWidget = IconWidget(FluentIcon.SPEED_OFF)
        # titleLabel = BodyLabel("环境模式", self.envcard)
        # items = ["跟随项目", "跟随设置", "独立模式"]
        # comboBox = ComboBox(self.envcard)
        # comboBox.addItems(items)
        # self.hBoxLayout.addWidget(iconWidget)
        # self.hBoxLayout.addWidget(titleLabel)
        # self.hBoxLayout.addStretch(1)
        # self.hBoxLayout.addWidget(comboBox, 0, Qt.AlignmentFlag.AlignRight)
        #
        # self.envcard = CardWidget(self)
        # self.hBoxLayout = QHBoxLayout(self.envcard)
        # iconWidget = IconWidget(FluentIcon.SPEED_OFF)
        # titleLabel = BodyLabel("环境模式", self.envcard)
        # items = ["跟随项目", "跟随设置", "独立模式"]
        # comboBox = ComboBox(self.envcard)
        # comboBox.addItems(items)
        # self.hBoxLayout.addWidget(iconWidget)
        # self.hBoxLayout.addWidget(titleLabel)
        # self.hBoxLayout.addStretch(1)
        # self.hBoxLayout.addWidget(comboBox, 0, Qt.AlignmentFlag.AlignRight)

        self.gridLayout1.addWidget(self.envcard, 1, 0, 1, 1)

        self.pyinstallerCard = SettingGroupCard(FluentIcon.SPEED_OFF, "Pyinstaller 设置", "",
                                                self.scrollAreaWidgetContents)
        widget = QWidget(self.pyinstallerCard)
        installLabel = BodyLabel("安装Pyinstaller环境")
        installBtn = PrimaryPushButton(self.pyinstallerCard)
        installBtn.setText("安装")
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(30, 5, 30, 5)
        layout.addWidget(installLabel)
        layout.addStretch(1)
        layout.addWidget(installBtn)
        self.pyinstallerCard.addWidget(widget)
        self.gridLayout1.addWidget(self.pyinstallerCard, 2, 0, 1, 1)

        self.nuitkaCard = SettingGroupCard(FluentIcon.SPEED_OFF, "Nuitka 设置", "",
                                                self.scrollAreaWidgetContents)
        widget = QWidget(self.nuitkaCard)
        installLabel = BodyLabel("安装Nuitka环境")
        installBtn = PrimaryPushButton(self.nuitkaCard)
        installBtn.setText("安装")
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(30, 5, 30, 5)
        layout.addWidget(installLabel)
        layout.addStretch(1)
        layout.addWidget(installBtn)
        self.nuitkaCard.addWidget(widget)
        self.gridLayout1.addWidget(self.nuitkaCard, 3, 0, 1, 1)








        self.verticalSpacer = QSpacerItem(0, 1000, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.gridLayout1.addItem(self.verticalSpacer, 4, 0, 1, 1)





