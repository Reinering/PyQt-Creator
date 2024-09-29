#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author: Reiner New
email: nbxlc@hotmail.com
Module implementing SettingWidget.
"""


from PySide6.QtCore import Slot, Qt, QThread, Signal
from PySide6.QtGui import QIcon, QFont
from PySide6.QtWidgets import QWidget, QGridLayout, QHBoxLayout, QVBoxLayout, QSpacerItem, QSizePolicy, QLabel
import os
from copy import copy
import logging

from qfluentwidgets import (
    BodyLabel, CaptionLabel,
    ComboBox,
    PrimaryPushButton,  PrimaryDropDownPushButton, PrimaryDropDownToolButton,
    Theme,
    RoundMenu, Action
)
from qfluentwidgets.common.icon import FluentIcon
from qfluentwidgets.common.style_sheet import FluentStyleSheet, getStyleSheetFromFile

from qfluentexpand.components.card.settingcard import SettingGroupCard, FileSelectorSettingCard
from qfluentexpand.components.line.selector import FilePathSelector, FolderPathSelector
from qfluentexpand.components.label.label import GifLabel
from qfluentexpand.common.gif import FluentGif
from .compoments.info import Message
from .Ui_SettingWidget import Ui_Form
from .utils.stylesheets import StyleSheet
from .utils.config import write_config
from common.pyenv import PyVenvManager
from common.py import PyInterpreter, PyPath
from manage import LIBS, MIRRORS, SETTINGS, CURRENT_SETTINGS


class SettingWidget(QWidget, Ui_Form):
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

        self.setObjectName("setting")
        StyleSheet.SETTING.apply(self)

        self.gridLayout1 = QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout1.setObjectName(u"gridLayout")
        self.gridLayout1.setContentsMargins(50, -1, 50, -1)
        self.gridLayout1.setSpacing(20)
        self.gridLayout1.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.venvMangerTh = VenvManagerThread()
        self.venvMangerTh.signal_result.connect(self.receive_VMresult)

        self.initWidget()

        self.venvMangerTh.setCMD("init")
        self.venvMangerTh.start()


    def initWidget(self):
        self.basicCard = SettingGroupCard(FluentIcon.SPEED_OFF, "基本设置", "",
                                          self.scrollAreaWidgetContents)

        self.gridLayout1.addWidget(self.basicCard, 1, 0, 1, 1)

        self.envCard = SettingGroupCard(FluentIcon.SPEED_OFF, "环境设置", "",
                                        self.scrollAreaWidgetContents)
        self.gridLayout1.addWidget(self.envCard, 2, 0, 1, 1)
        widget_mode = QWidget(self.envCard)
        envLabel = BodyLabel("模式 (全局)")
        self.comboBox_mode = ComboBox(self.envCard)
        self.comboBox_mode.addItems(SETTINGS["settings"]["python_env_modes"])
        self.comboBox_mode.currentTextChanged.connect(self.on_comboBox_mode_currentTextChanged)
        layout = QHBoxLayout(widget_mode)
        layout.setContentsMargins(30, 5, 30, 5)
        layout.addWidget(envLabel)
        layout.addStretch(1)
        layout.addWidget(self.comboBox_mode)
        self.envCard.addWidget(widget_mode)

        self.widget_env = QWidget(self.envCard)
        label_env = BodyLabel("Python 环境", self.envCard)
        self.label_ver = CaptionLabel("版本: ", self.envCard)
        self.button_filepath = FilePathSelector(self.envCard)
        self.button_filepath.setFileTypes("python.exe")
        self.button_filepath.setFixedWidth(200)
        self.button_filepath.textChanged.connect(self.on_button_filepath_textChanged)
        layout = QHBoxLayout(self.widget_env)
        layout.setContentsMargins(30, 5, 30, 5)
        layout.addWidget(label_env)
        layout.addStretch(1)
        layout.addWidget(self.label_ver)
        layout.addStretch(1)
        layout.addWidget(self.button_filepath)
        self.envCard.addWidget(self.widget_env)

        self.card_pyenv = SettingGroupCard(FluentIcon.SPEED_OFF, "Pyenv 虚拟环境管理", "https://github.com/pyenv-win/pyenv-win",
                                          self.scrollAreaWidgetContents)
        self.gridLayout1.addWidget(self.card_pyenv, 3, 0, 1, 1)

        self.widget_pyenv_path = QWidget(self.card_pyenv)
        hBoxLayout = QHBoxLayout(self.widget_pyenv_path)
        hBoxLayout.setContentsMargins(30, 0, 30, 0)
        hBoxLayout.setSpacing(0)
        hBoxLayout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        vBoxLayout = QVBoxLayout(self.widget_pyenv_path)
        vBoxLayout.setSpacing(0)
        vBoxLayout.setContentsMargins(0, 0, 0, 0)
        vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        label_pyenv_path = BodyLabel("pyenv-win 根目录")
        # label_content = QLabel('asdfas' or '', self)
        # label_content.setFont(QFont("5px 'Segoe UI', 'Microsoft YaHei', 'PingFang SC'"))
        # contentLabel.setStyleSheet({"font": "11px 'Segoe UI', 'Microsoft YaHei', 'PingFang SC'",
        #                             "color": "rgb(96, 96, 96)",
        #                             "padding": "0"
        #                             })

        hBoxLayout.addLayout(vBoxLayout)
        vBoxLayout.addWidget(label_pyenv_path, 0, Qt.AlignmentFlag.AlignLeft)
        # vBoxLayout.addWidget(label_content, 0, Qt.AlignmentFlag.AlignLeft)
        hBoxLayout.addSpacing(16)
        hBoxLayout.addStretch(1)

        self.button_pyenv_path = FolderPathSelector(self.envCard)
        self.button_pyenv_path.setFixedWidth(200)
        self.button_pyenv_path.textChanged.connect(self.on_button_pyenv_path_textChanged)
        hBoxLayout.addWidget(self.button_pyenv_path)

        self.card_pyenv.addWidget(self.widget_pyenv_path)

        self.widget_pyenv_existing = QWidget(self.card_pyenv)
        label_existing = BodyLabel("现有环境")
        self.spinner_existing = GifLabel(self.card_pyenv)
        self.spinner_existing.setGif(FluentGif.LOADING.path())
        self.spinner_existing.setFixedSize(30, 30)
        self.spinner_existing.hide()
        self.comboBox_existing = ComboBox(self.card_pyenv)
        self.comboBox_existing.setMinimumWidth(100)
        self.comboBox_existing.currentTextChanged.connect(self.on_comboBox_existing_currentTextChanged)

        self.button_existing_uninstall = PrimaryDropDownPushButton(FluentIcon.MAIL, '操作')
        menu = RoundMenu(parent=self.button_existing_uninstall)
        menu.addAction(Action(FluentIcon.BASKETBALL, '更新', triggered=self.existing_update))
        menu.addAction(Action(FluentIcon.ALBUM, '卸载', triggered=self.existing_uninstall))
        self.button_existing_uninstall.setMenu(menu)

        layout = QHBoxLayout(self.widget_pyenv_existing)
        layout.setContentsMargins(30, 5, 30, 5)
        layout.addWidget(label_existing)
        layout.addStretch(1)
        layout.addWidget(self.spinner_existing)
        layout.addWidget(self.comboBox_existing)
        layout.addWidget(self.button_existing_uninstall)
        self.card_pyenv.addWidget(self.widget_pyenv_existing)

        self.widget_pyenv_new = QWidget(self.card_pyenv)
        label_new = BodyLabel("安装新环境")
        self.spinner_new = GifLabel(self.card_pyenv)
        self.spinner_new.setGif(FluentGif.LOADING.path())
        self.spinner_new.setFixedSize(30, 30)
        self.spinner_new.hide()
        self.comboBox_new_maxbit = ComboBox(self.card_pyenv)
        self.comboBox_new_maxbit.addItems(SETTINGS["settings"]["pyenv_maxbit"])
        self.comboBox_new_maxbit.setFixedWidth(75)
        self.comboBox_new_ver = ComboBox(self.card_pyenv)
        self.comboBox_new_ver.setMinimumWidth(100)

        self.button_new_install = PrimaryDropDownPushButton(FluentIcon.MAIL, '操作')
        menu = RoundMenu(parent=self.button_new_install)
        menu.addAction(Action(FluentIcon.BASKETBALL, '安装', triggered=self.new_install))
        menu.addAction(Action(FluentIcon.ALBUM, '更新', triggered=self.new_update))
        self.button_new_install.setMenu(menu)

        layout = QHBoxLayout(self.widget_pyenv_new)
        layout.setContentsMargins(30, 5, 30, 5)
        layout.addWidget(label_new)
        layout.addStretch(1)
        layout.addWidget(self.spinner_new)
        layout.addWidget(self.comboBox_new_maxbit)
        layout.addWidget(self.comboBox_new_ver)
        layout.addWidget(self.button_new_install)
        self.card_pyenv.addWidget(self.widget_pyenv_new)

        self.widget_pyenv_mirror_url = QWidget(self.card_pyenv)
        label_mirror_url = BodyLabel("更新源")
        self.comboBox_pyenv_mirror_url = ComboBox(self.card_pyenv)
        self.comboBox_pyenv_mirror_url.setMinimumWidth(100)
        self.comboBox_pyenv_mirror_url.setMaximumWidth(150)
        self.comboBox_pyenv_mirror_url.addItems(MIRRORS["pyenv"].keys())
        self.comboBox_pyenv_mirror_url.currentTextChanged.connect(self.on_comboBox_pyenv_mirror_url_currentTextChanged)

        layout = QHBoxLayout(self.widget_pyenv_mirror_url)
        layout.setContentsMargins(30, 5, 30, 5)
        layout.addWidget(label_mirror_url)
        layout.addWidget(self.comboBox_pyenv_mirror_url)
        self.card_pyenv.addWidget(self.widget_pyenv_mirror_url)

        self.card_pip = SettingGroupCard(FluentIcon.SPEED_OFF, "Pip 设置", "",
                                           self.scrollAreaWidgetContents)
        self.gridLayout1.addWidget(self.card_pip, 4, 0, 1, 1)

        self.widget_pip_mirror_url = QWidget(self.card_pip)
        label_mirror_url = BodyLabel("更新源")
        self.comboBox_pip_mirror_url = ComboBox(self.card_pip)
        self.comboBox_pip_mirror_url.setMinimumWidth(100)
        self.comboBox_pip_mirror_url.setMaximumWidth(150)
        self.comboBox_pip_mirror_url.addItems(MIRRORS["pip"].keys())
        self.comboBox_pip_mirror_url.currentTextChanged.connect(self.on_comboBox_pip_mirror_url_currentTextChanged)

        layout = QHBoxLayout(self.widget_pip_mirror_url)
        layout.setContentsMargins(30, 5, 30, 5)
        layout.addWidget(label_mirror_url)
        layout.addWidget(self.comboBox_pip_mirror_url)
        self.card_pip.addWidget(self.widget_pip_mirror_url)


        self.infoCard = SettingGroupCard(FluentIcon.SPEED_OFF, "帮助", "",
                                         self.scrollAreaWidgetContents)

        self.gridLayout1.addWidget(self.infoCard, 5, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(0, 1000, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.gridLayout1.addItem(self.verticalSpacer)


        self.configure()

    def configure(self):

        if CURRENT_SETTINGS["settings"]["mode"] in SETTINGS["settings"]["python_env_modes"]:
            self.comboBox_mode.setCurrentText(CURRENT_SETTINGS["settings"]["mode"])

        if CURRENT_SETTINGS["settings"]["custom_python_path"]:
            self.button_filepath.setText(CURRENT_SETTINGS["settings"]["custom_python_path"])

        if CURRENT_SETTINGS["settings"]["pyenv_path"]:
            self.button_pyenv_path.setText(CURRENT_SETTINGS["settings"]["pyenv_path"])
        else:
            self.button_pyenv_path.setText(LIBS["pyenv"])

        if CURRENT_SETTINGS["settings"]["pyenv_current_version"]:
            self.comboBox_existing.setText(CURRENT_SETTINGS["settings"]["pyenv_current_version"])

        if CURRENT_SETTINGS["settings"]["pyenv_mirror_url"]:
            self.comboBox_pyenv_mirror_url.setText(CURRENT_SETTINGS["settings"]["pyenv_mirror_url"])

        if CURRENT_SETTINGS["settings"]["pip_mirror_url"]:
            self.comboBox_pip_mirror_url.setText(CURRENT_SETTINGS["settings"]["pip_mirror_url"])

    def new_install(self):
        version = self.comboBox_new_ver.currentText()
        if not version:
            return

        if self.comboBox_new_maxbit.currentText() == "x86":
            version += "-win32"

        if self.venvMangerTh.isRunning():
            Message.error("错误", "pyenv忙碌中，请稍后重试", self)
            return

        self.venvMangerTh.setCMD("install", version)
        self.venvMangerTh.start()
        self.button_new_install.setEnabled(False)
        self.spinner_new.setState(True)
        self.spinner_new.show()
        Message.info("安装", "安装中，请稍后", self)

    def new_update(self):
        if self.venvMangerTh.isRunning():
            Message.error("错误", "pyenv忙碌中，请稍后重试", self)
            return

        self.venvMangerTh.setCMD("update")
        self.venvMangerTh.start()
        self.button_new_install.setEnabled(False)
        self.spinner_new.setState(True)
        self.spinner_new.show()

    def existing_uninstall(self):
        if self.comboBox_existing.currentText():
            if self.venvMangerTh.isRunning():
                Message.error("错误", "pyenv忙碌中，请稍后重试", self)
                return

            self.venvMangerTh.setCMD("uninstall", self.comboBox_existing.currentText())
            self.venvMangerTh.start()
            self.button_existing_uninstall.setEnabled(False)
            self.spinner_existing.show()
            self.spinner_existing.setState(True)
            Message.info("卸载", "卸载中，请稍后", self)

    def existing_update(self):
        if os.path.exists(os.path.join(LIBS["pyenv"], "versions")):
            if self.venvMangerTh.isRunning():
                Message.error("错误", "pyenv忙碌中，请稍后重试", self)
                return

            self.venvMangerTh.setCMD("versions")
            self.venvMangerTh.start()
            self.button_existing_uninstall.setEnabled(False)
            self.spinner_existing.setState(True)
            self.spinner_existing.show()

    def on_comboBox_mode_currentTextChanged(self, text):
        CURRENT_SETTINGS["settings"]["mode"] = text
        if text == "现有环境":
            self.widget_env.show()
            self.card_pyenv.hide()
        elif text == "Pyenv 环境":
            self.widget_env.hide()
            self.card_pyenv.show()
        else:
            pass

        write_config()

    def on_button_filepath_textChanged(self, text):
        if text and "python.exe" in text:
            self.venvMangerTh.setPyInterpreter(text)
            self.venvMangerTh.setCMD("py_version")
            self.venvMangerTh.start()
        else:
            self.label_ver.setText("版本: ")
            CURRENT_SETTINGS["settings"]["custom_python_path"] = ""
            write_config()

    def on_button_pyenv_path_textChanged(self, text):
        if text:
            CURRENT_SETTINGS["settings"]["pyenv_path"] = text
            write_config()

    def on_comboBox_existing_currentTextChanged(self, text):
        CURRENT_SETTINGS["settings"]["pyenv_current_version"] = text

        write_config()

    def on_comboBox_pyenv_mirror_url_currentTextChanged(self, text):
        CURRENT_SETTINGS["settings"]["pyenv_mirror_url"] = text
        if text != "origin" and MIRRORS["pyenv"].get(text):
            if self.venvMangerTh.isRunning():
                Message.error("错误", "pyenv忙碌中，请稍后重试", self)
                return

            self.venvMangerTh.setCMD("environ", PYTHON_BUILD_MIRROR_URL=MIRRORS["pyenv"][text])
            self.venvMangerTh.start()

            write_config()

    def on_comboBox_pip_mirror_url_currentTextChanged(self, text):
        CURRENT_SETTINGS["settings"]["pip_mirror_url"] = text

        write_config()

    def on_button_existing_uninstall_clicked(self):
        if self.comboBox_existing.currentText():
            if self.venvMangerTh.isRunning():
                Message.error("错误", "pyenv忙碌中，请稍后重试", self)
                return

            self.venvMangerTh.setCMD("uninstall", self.comboBox_existing.currentText())
            self.venvMangerTh.start()
            self.button_existing_uninstall.setEnabled(False)
            self.spinner_existing.show()
            self.spinner_existing.setState(True)
            Message.info("卸载", "卸载中，请稍后", self)

    def receive_VMresult(self, cmd, result):
        logging.debug(f"receive_VMresult: {cmd}, {result}")
        if cmd == "py_version":
            if not result[0]:
                Message.error("解释器错误", result[1], self)
                return
            self.label_ver.setText("版本: " + result[1])
            CURRENT_SETTINGS["other"]["custom_python_path"] = self.button_filepath.text()
            write_config()
        elif cmd == "list":
            if not result[0]:
                Message.error("错误", result[1], self)
                return
            result = list(filter(None, result[1].split("\n")[1:]))
            result.reverse()
            tmp = copy(result)
            for res in tmp:
                if "rc" in res or "a" in res or "b" in res or 'c' in res or 'win32' in res:
                    result.remove(res)
            if result:
                self.comboBox_new_ver.clear()
                self.comboBox_new_ver.addItems(result)
        elif cmd == "update":
            self.button_new_install.setEnabled(True)
            self.spinner_new.setState(False)
            self.spinner_new.hide()

            if not result[0]:
                Message.error("错误", result[1], self)
                return

            self.venvMangerTh.setCMD("list")
            self.venvMangerTh.start()
        elif cmd == "install":
            self.button_new_install.setEnabled(True)
            self.spinner_new.setState(False)
            self.spinner_new.hide()

            if not result[0]:
                Message.error("错误", result[1], self)
                return

            Message.info("成功", "安装成功", self)
            self.existing_update()
        elif cmd == "uninstall":
            self.button_existing_uninstall.setEnabled(True)
            self.spinner_existing.setState(False)
            self.spinner_existing.hide()

            if not result[0]:
                Message.error("错误", result[1], self)
                return

            Message.info("成功", "卸载成功", self)
        elif cmd == "versions":
            self.button_existing_uninstall.setEnabled(True)
            self.spinner_existing.setState(False)
            self.spinner_existing.hide()

            if not result[0]:
                Message.error("错误", result[1], self)
                return

            result = list(filter(None, result[1].split("\n")))
            tmp = []
            for res in result:
                res.strip()
                tmp.append(res.strip())
            if result:
                self.comboBox_existing.clear()
                self.comboBox_existing.addItems(tmp)
        else:
            pass


class VenvManagerThread(QThread):

    signal_result = Signal(str, tuple)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.venvManger = PyVenvManager(LIBS["pyenv"])
        self.pyI = PyInterpreter()
        self.stop = False

    def stop(self):
        self.stop = True

    def setCMD(self, cmd, *args, **kwargs):
        self.cmd = cmd
        self.args = args
        self.kwargs = kwargs

    def setPyInterpreter(self, path):
        self.pyI.setInterpreter(path)

    def run(self):
        if self.cmd == "py_version":
            result = self.pyI.version()
            self.signal_result.emit(self.cmd, result)
        elif self.cmd == "init":
            result = self.venvManger.list()
            self.signal_result.emit("list", result)
            result = self.venvManger.versions()
            self.signal_result.emit("versions", result)
        elif self.cmd == "list":
            result = self.venvManger.list()
            self.signal_result.emit(self.cmd, result)
        elif self.cmd == "update":
            result = self.venvManger.update()
            self.signal_result.emit(self.cmd, result)
        elif self.cmd == "install":
            result = self.venvManger.install(self.args[0])
            self.signal_result.emit(self.cmd, result)
            self.venvManger.rehash()
        elif self.cmd == "uninstall":
            result = self.venvManger.uninstall(self.args[0])
            self.signal_result.emit(self.cmd, result)
        elif self.cmd == "environ":
            self.venvManger.setEnviron(**self.kwargs)
        elif self.cmd == "versions":
            result = self.venvManger.versions()
            self.signal_result.emit(self.cmd, result)
        else:
            self.signal_result.emit(self.cmd, ["False", "未知命令"])



