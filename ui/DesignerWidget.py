#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author: Reiner New
email: nbxlc@hotmail.com
Module implementing DesignerWidget.
"""


from PySide6.QtCore import Slot, Qt, QRect
from PySide6.QtWidgets import QWidget, QGridLayout, QHBoxLayout, QVBoxLayout, QSpacerItem, QSizePolicy

from qfluentwidgets import (
    ScrollArea,
    PrimaryPushButton,
    ComboBox,
    BodyLabel, TitleLabel, CaptionLabel,
    CardWidget,
    IconWidget,
    SettingCard,
)
from qfluentwidgets.common.icon import FluentIcon
from qfluentwidgets.components.settings.setting_card import SettingIconWidget

from qfluentexpand.components.card.settingcard import SettingGroupCard, ComboBoxSettingCard
from qfluentexpand.components.line.selector import FilePathSelector

from .Ui_DesignerWidget import Ui_Form
from .utils.stylesheets import StyleSheet


class DesignerWidget(QWidget, Ui_Form):
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
        self.setObjectName("designer")
        StyleSheet.DESIGNER.apply(self)

        self.gridLayout1 = QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout1.setObjectName(u"gridLayout1")
        self.gridLayout1.setContentsMargins(50, -1, 50, -1)
        self.gridLayout1.setSpacing(20)
        self.gridLayout1.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.initTitle()
        self.initWidget()

    def initTitle(self):
        self.titleCard = CardWidget(self)
        self.titleCard.setMinimumHeight(200)
        self.gridLayout1.addWidget(self.titleCard, 0, 0, 1, 1)
        # self.ScrollArea.setViewportMargins(0, self.titleCard.height(), 0, 0)
        self.ScrollArea.setWidgetResizable(True)

        titleLabel = TitleLabel("Designer", self)
        subtitleLabel = CaptionLabel("PySide Designer", self)

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
        self.envCard = ComboBoxSettingCard(FluentIcon.SPEED_OFF, "环境模式", '', self.scrollAreaWidgetContents)
        self.envCard.addItems(["跟随项目", "跟随全局", "独立模式"])

        # self.envCard = CardWidget(self)
        # self.hBoxLayout = QHBoxLayout(self.envCard)
        # self.hBoxLayout.setSpacing(0)
        # self.hBoxLayout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        #
        # iconWidget = SettingIconWidget(FluentIcon.SPEED_OFF, self.envCard)
        # iconWidget.setFixedSize(16, 16)
        # titleLabel = BodyLabel("环境模式", self.envCard)
        # items = ["跟随项目", "跟随全局", "独立模式"]
        # comboBox = ComboBox(self.envCard)
        # comboBox.addItems(items)
        # self.hBoxLayout.addWidget(iconWidget)
        # self.hBoxLayout.addSpacing(16)
        # self.hBoxLayout.addWidget(titleLabel)
        # self.hBoxLayout.addStretch(1)
        # self.hBoxLayout.addWidget(comboBox, 0, Qt.AlignmentFlag.AlignRight)

        self.gridLayout1.addWidget(self.envCard, 1, 0, 1, 1)


        self.designerSetCard = SettingGroupCard(FluentIcon.SPEED_OFF, "Desinger 设置", "",
                                                self.scrollAreaWidgetContents)
        widget = QWidget(self.designerSetCard)
        envLabel = BodyLabel("Python 环境")
        envButton = FilePathSelector(self.designerSetCard)
        envButton.setText("选择")
        envButton.setFileTypes("python.exe")
        envButton.setFixedWidth(200)
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(30, 5, 30, 5)
        layout.addWidget(envLabel)
        layout.addStretch(1)
        layout.addWidget(envButton)
        self.designerSetCard.addWidget(widget)

        widget = QWidget(self.designerSetCard)
        installLabel = BodyLabel("安装Designer环境")
        installBtn = PrimaryPushButton(self.designerSetCard)
        installBtn.setText("安装")
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(30, 5, 30, 5)
        layout.addWidget(installLabel)
        layout.addStretch(1)
        layout.addWidget(installBtn)
        self.designerSetCard.addWidget(widget)
        self.gridLayout1.addWidget(self.designerSetCard, 2, 0, 1, 1)

        # setting = SettingCard(FluentIcon.SPEED_OFF, "Desinger 设置", "", self.scrollAreaWidgetContents)
        # self.gridLayout1.addWidget(setting, 3, 0, 1, 1)


        self.verticalSpacer = QSpacerItem(0, 1000, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.gridLayout1.addItem(self.verticalSpacer, 3, 0, 1, 1)


