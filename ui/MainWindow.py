#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author: Reiner New
email: nbxlc@hotmail.com
Module implementing MainWindow.
"""


from PySide6.QtCore import Slot, QThread
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget, QGridLayout
import os

from qfluentwidgets import NavigationItemPosition, PipsPager
from qfluentwidgets.common.icon import isDarkTheme, FluentIconBase, FluentIcon as FIF

from qfluentexpand.window.fluent_window import FluentWindow

from .Ui_MainWindow import Ui_Form
from .HomeWidget import HomeWidget
from .ProjectWidget import ProjectWidget
from .DesignerWidget import DesignerWidget
from .PackWidget import PackWidget
from .DocumentWidget import DocumentWidget
from .SettingWidget import SettingWidget
from .ConsoleWidget import ConsoleWidget
from .OtherWidget import OtherWidget

from .utils.icon import AppIcon
from .utils.stylesheets import StyleSheet
from manage import APPNAME, UI_CONFIG, RUNTIMEENV, BUNDLE_DIR, PAGEWidgets


class MainWindow(FluentWindow, Ui_Form):
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

        self.initNavi()

        self.initWidget()

    def initNavi(self):
        # navigator setting
        # self.navigationInterface.setMenuButtonVisible(False)
        self.navigationInterface.setReturnButtonVisible(False)

        # enable acrylic effect
        self.navigationInterface.setAcrylicEnabled(True)

        # 展开宽度 宽度会影响导航栏的展开与折叠效果
        self.navigationInterface.panel.setExpandWidth(150)

        PAGEWidgets["main"] = self
        PAGEWidgets["navi"] = self.navigationInterface

        # create sub interface
        self.home = HomeWidget(self)
        PAGEWidgets["home"] = self.home

        self.project = ProjectWidget(self)
        PAGEWidgets["project"] = self.project

        self.designer = DesignerWidget(self)
        PAGEWidgets["designer"] = self.designer

        self.pack = PackWidget(self)
        PAGEWidgets["pack"] = self.pack

        self.other = OtherWidget(self)
        PAGEWidgets["other"] = self.other

        self.console = ConsoleWidget(self)
        PAGEWidgets["console"] = self.console

        self.document = DocumentWidget(self)
        PAGEWidgets["document"] = self.document

        self.settings = SettingWidget(self)
        PAGEWidgets["settings"] = self.settings

        self.addSubInterface(
            self.home,
            AppIcon.HOME,
            "Home",
            NavigationItemPosition.SCROLL
        )
        self.addSubInterface(
            self.project,
            AppIcon.PROJECT,
            "Project",
            NavigationItemPosition.SCROLL
        )
        self.addSubInterface(
            self.designer,
            AppIcon.DESIGNER,
            "Designer",
            NavigationItemPosition.SCROLL
        )
        self.addSubInterface(
            self.pack,
            AppIcon.PACK,
            "Pack",
            NavigationItemPosition.SCROLL
        )
        self.addSubInterface(
            self.other,
            AppIcon.OTHER,
            "Other",
            NavigationItemPosition.SCROLL
        )
        self.addSubInterface(
            self.console,
            AppIcon.CONSOLE,
            "Console",
            NavigationItemPosition.SCROLL
        )

        self.navigationInterface.addSeparator()

        self.addSubInterface(
            self.document,
            AppIcon.DOCUMENT,
            "Document",
            NavigationItemPosition.BOTTOM
        )
        self.addSubInterface(
            self.settings,
            AppIcon.SETTINGS,
            "Settings",
            NavigationItemPosition.BOTTOM
        )

    def initWidget(self):
        self.resize(900, 700)
        self.setWindowTitle(APPNAME)
        self.setWindowIcon(QIcon(UI_CONFIG["logoPath"]))
        # self.setWindowIcon(QIcon(f':/logo/images/logo.png'))

        StyleSheet.MAIN.apply(self)


class PyThread(QThread):

    def __init__(self, parent=None):
        super().__init__(parent)

    def run(self):
        pass
