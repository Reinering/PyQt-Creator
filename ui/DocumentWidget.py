# -*- coding: utf-8 -*-

"""
Module implementing DocumentWidget.
"""


from PySide6.QtCore import Slot, QRect, Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget, QGridLayout, QHBoxLayout, QVBoxLayout, QSpacerItem, QSizePolicy


from qfluentwidgets import (
    ExpandGroupSettingCard,
    PrimaryPushButton, PrimaryDropDownPushButton,
    BodyLabel, TitleLabel, CaptionLabel,
    ScrollArea,
    CardWidget, IconWidget, ComboBox,
    RoundMenu,
    Action
)
from qfluentwidgets.common.icon import isDarkTheme, FluentIconBase, FluentIconBase as FIF, FluentIcon

from qfluentexpand.components.card.settingcard import SettingGroupCard
from qfluentexpand.components.label.label import GifLabel
from qfluentexpand.common.gif import FluentGif

from .Ui_DocumentWidget import Ui_Form
from .utils.stylesheets import StyleSheet



class DocumentWidget(QWidget, Ui_Form):
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
        self.setObjectName("document")
        StyleSheet.DOCUMENT.apply(self)

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

        titleLabel = TitleLabel("Document", self)
        subtitleLabel = CaptionLabel("文档", self)

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

    def initWidget(self):
        self.card_pyinstaller = SettingGroupCard(FluentIcon.SPEED_OFF, "pyinstaller", "",
                                        self.scrollAreaWidgetContents)
        self.gridLayout1.addWidget(self.card_pyinstaller, 1, 0, 1, 1)




        self.card_nuitka = SettingGroupCard(FluentIcon.SPEED_OFF, "nuitka", "",
                                                 self.scrollAreaWidgetContents)
        self.gridLayout1.addWidget(self.card_nuitka, 2, 0, 1, 1)




        self.card_nuitka = SettingGroupCard(FluentIcon.SPEED_OFF, "pipreqs", "",
                                            self.scrollAreaWidgetContents)
        self.gridLayout1.addWidget(self.card_nuitka, 3, 0, 1, 1)




        verticalSpacer = QSpacerItem(0, 1000, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.gridLayout1.addItem(verticalSpacer, 4, 0, 1, 1)