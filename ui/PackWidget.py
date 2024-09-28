#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author: Reiner New
email: nbxlc@hotmail.com
Module implementing PackWidget.
"""


from PySide6.QtCore import Slot, QRect, Qt, QThread, Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget, QGridLayout, QHBoxLayout, QVBoxLayout, QSpacerItem, QSizePolicy
import os
import datetime
import simplejson as json
from pathlib import Path

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
from qfluentexpand.components.line.selector import FilePathSelector, FolderPathSelector
from qfluentexpand.components.label.label import GifLabel
from qfluentexpand.common.gif import FluentGif

from .Ui_PackWidget import Ui_Form
from .utils.stylesheets import StyleSheet
from .utils.config import write_config
from .compoments.info import Message
from common.pyenv import PyVenvManager
from common.py import PyInterpreter, PyPath
from common.pyinstaller import PyinstallerPackage
from common.nuitka import NuitkaPackage
from manage import ROOT_PATH, SettingPath, LIBS, SETTINGS, CURRENT_SETTINGS, REQUIREMENTS_URLS


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

        self.venvMangerTh = VenvManagerThread()
        self.venvMangerTh.signal_result.connect(self.receive_VMresult)

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

        layout = QHBoxLayout(self.titleCard)
        layout.setSpacing(10)

        horizontalSpacer = QSpacerItem(1000, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.spinner_open = GifLabel(self.titleCard)
        self.spinner_open.setGif(FluentGif.LOADING.path())
        self.spinner_open.setFixedSize(30, 30)
        self.spinner_open.hide()
        self.button_open = PrimaryDropDownPushButton(FluentIcon.MAIL, '打包')
        menu = RoundMenu(parent=self.button_open)
        menu.addAction(Action(FluentIcon.BASKETBALL, 'pyinstaller', triggered=self.open_pyinstaller))
        menu.addAction(Action(FluentIcon.ALBUM, 'nuitka', triggered=self.open_nuitka))
        self.button_open.setMenu(menu)

        layout.addItem(horizontalSpacer)
        layout.addWidget(self.spinner_open)
        layout.addWidget(self.button_open)
        hBoxLayout.addLayout(layout, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

    def initWidget(self):
        self.envCard = SettingGroupCard(FluentIcon.SPEED_OFF, "环境设置", "",
                                        self.scrollAreaWidgetContents)
        self.gridLayout1.addWidget(self.envCard, 1, 0, 1, 1)
        widget_mode = QWidget(self.envCard)
        envLabel = BodyLabel("模式")
        self.comboBox_mode = ComboBox(self.envCard)
        self.comboBox_mode.addItems(SETTINGS["pack"]["python_env_modes"])
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

        self.widget_env_main = QWidget(self.envCard)
        label_env = BodyLabel("程序入口", self.envCard)
        self.button_filepath_main = FilePathSelector(self.envCard)
        self.button_filepath_main.setFileTypes("python(*.py)")
        self.button_filepath_main.setMaximumWidth(300)
        self.button_filepath_main.setFixedWidth(200)
        self.button_filepath_main.textChanged.connect(self.on_button_filepath_main_textChanged)
        layout = QHBoxLayout(self.widget_env_main)
        layout.setContentsMargins(30, 5, 30, 5)
        layout.addWidget(label_env)
        layout.addStretch(1)
        layout.addWidget(self.button_filepath_main)
        self.envCard.addWidget(self.widget_env_main)

        self.widget_env_out = QWidget(self.envCard)
        label_env = BodyLabel("输出目录", self.envCard)
        self.button_filepath_out = FolderPathSelector(self.envCard)
        self.button_filepath_out.setPlaceholderText("默认为程序入口目录")
        self.button_filepath_out.setMaximumWidth(300)
        self.button_filepath_out.setFixedWidth(200)
        self.button_filepath_out.textChanged.connect(self.on_button_filepath_out_textChanged)
        layout = QHBoxLayout(self.widget_env_out)
        layout.setContentsMargins(30, 5, 30, 5)
        layout.addWidget(label_env)
        layout.addStretch(1)
        layout.addWidget(self.button_filepath_out)
        self.envCard.addWidget(self.widget_env_out)

        self.card_pyinstaller = SettingGroupCard(FluentIcon.SPEED_OFF, "Pyinstaller 设置", "",
                                                self.scrollAreaWidgetContents)
        self.gridLayout1.addWidget(self.card_pyinstaller, 2, 0, 1, 1)
        widget_pyinstaller = QWidget(self.card_pyinstaller)
        label_pyinstaller = BodyLabel("Pyinstaller 模块")
        self.spinner_pyinstaller = GifLabel(self.card_pyinstaller)
        self.spinner_pyinstaller.setGif(FluentGif.LOADING.path())
        self.spinner_pyinstaller.setFixedSize(30, 30)
        self.spinner_pyinstaller.hide()
        self.button_pyinstaller = PrimaryDropDownPushButton(FluentIcon.MAIL, '操作')
        menu = RoundMenu(parent=self.button_pyinstaller)
        menu.addAction(Action(FluentIcon.BASKETBALL, '安装', triggered=self.pyinstaller_install))
        menu.addAction(Action(FluentIcon.ALBUM, '更新', triggered=self.pyinstaller_upgrade))
        menu.addAction(Action(FluentIcon.ALBUM, '卸载', triggered=self.pyinstaller_uninstall))
        self.button_pyinstaller.setMenu(menu)

        layout = QHBoxLayout(widget_pyinstaller)
        layout.setContentsMargins(30, 5, 30, 5)
        layout.addWidget(label_pyinstaller)
        layout.addStretch(1)
        layout.addWidget(self.spinner_pyinstaller)
        layout.addWidget(self.button_pyinstaller)
        self.card_pyinstaller.addWidget(widget_pyinstaller)

        widget_pyinstaller_settingfile = QWidget(self.card_pyinstaller)
        label_pyinstaller = BodyLabel("pyinstaller 配置文件")
        self.spinner_pyinstaller_settingfile = GifLabel(self.card_pyinstaller)
        self.spinner_pyinstaller_settingfile.setGif(FluentGif.LOADING.path())
        self.spinner_pyinstaller_settingfile.setFixedSize(30, 30)
        self.spinner_pyinstaller_settingfile.hide()
        self.button_pyinstaller_settingfile = PrimaryPushButton(self.card_pyinstaller)
        self.button_pyinstaller_settingfile.setText("编辑")
        self.button_pyinstaller_settingfile.clicked.connect(self.on_button_pyinstaller_settingfile_clicked)
        layout = QHBoxLayout(widget_pyinstaller_settingfile)
        layout.setContentsMargins(30, 5, 30, 5)
        layout.addWidget(label_pyinstaller)
        layout.addStretch(1)
        layout.addWidget(self.spinner_pyinstaller_settingfile)
        layout.addWidget(self.button_pyinstaller_settingfile)
        self.card_pyinstaller.addWidget(widget_pyinstaller_settingfile)

        self.card_nuitka = SettingGroupCard(FluentIcon.SPEED_OFF, "Nuitka 设置", "",
                                                self.scrollAreaWidgetContents)
        self.gridLayout1.addWidget(self.card_nuitka, 3, 0, 1, 1)
        widget_nuitka = QWidget(self.card_nuitka)
        label_nuitka = BodyLabel("Nuitka 模块")
        self.spinner_nuitka = GifLabel(self.card_nuitka)
        self.spinner_nuitka.setGif(FluentGif.LOADING.path())
        self.spinner_nuitka.setFixedSize(30, 30)
        self.spinner_nuitka.hide()
        self.button_nuitka = PrimaryDropDownPushButton(FluentIcon.MAIL, '操作')
        menu = RoundMenu(parent=self.button_nuitka)
        menu.addAction(Action(FluentIcon.BASKETBALL, '安装', triggered=self.nuitka_install))
        menu.addAction(Action(FluentIcon.ALBUM, '更新', triggered=self.nuitka_upgrade))
        menu.addAction(Action(FluentIcon.ALBUM, '卸载', triggered=self.nuitka_uninstall))
        self.button_nuitka.setMenu(menu)

        layout = QHBoxLayout(widget_nuitka)
        layout.setContentsMargins(30, 5, 30, 5)
        layout.addWidget(label_nuitka)
        layout.addStretch(1)
        layout.addWidget(self.spinner_nuitka)
        layout.addWidget(self.button_nuitka)
        self.card_nuitka.addWidget(widget_nuitka)

        widget_nuitka_settingfile = QWidget(self.card_nuitka)
        label_nuitka = BodyLabel("nuitka 配置文件")
        self.spinner_nuitka_settingfile = GifLabel(self.card_nuitka)
        self.spinner_nuitka_settingfile.setGif(FluentGif.LOADING.path())
        self.spinner_nuitka_settingfile.setFixedSize(30, 30)
        self.spinner_nuitka_settingfile.hide()
        self.button_nuitka_settingfile = PrimaryPushButton(self.card_nuitka)
        self.button_nuitka_settingfile.setText("编辑")
        self.button_nuitka_settingfile.clicked.connect(self.on_button_nuitka_settingfile_clicked)
        layout = QHBoxLayout(widget_nuitka_settingfile)
        layout.setContentsMargins(30, 5, 30, 5)
        layout.addWidget(label_nuitka)
        layout.addStretch(1)
        layout.addWidget(self.spinner_nuitka_settingfile)
        layout.addWidget(self.button_nuitka_settingfile)
        self.card_nuitka.addWidget(widget_nuitka_settingfile)



        verticalSpacer = QSpacerItem(0, 1000, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.gridLayout1.addItem(verticalSpacer, 4, 0, 1, 1)

        self.configure()

    def configure(self):
        if CURRENT_SETTINGS["pack"]["mode"] in SETTINGS["pack"]["python_env_modes"]:
            self.comboBox_mode.setCurrentText(CURRENT_SETTINGS["pack"]["mode"])

        if CURRENT_SETTINGS["pack"]["custom_python_path"]:
            self.button_filepath.setText(CURRENT_SETTINGS["pack"]["custom_python_path"])

        if CURRENT_SETTINGS["pack"]["main"]:
            self.button_filepath_main.setText(CURRENT_SETTINGS["pack"]["main"])

        if CURRENT_SETTINGS["pack"]["outPath"]:
            self.button_filepath_out.setText(CURRENT_SETTINGS["pack"]["outPath"])

    def getPyPath(self):
        path = ""
        if self.comboBox_mode.currentText() == "独立模式":
            path = self.button_filepath.text()
            if not path:
                Message.error("错误", "请选择Python环境", self)
                return
        elif self.comboBox_mode.currentText() == "跟随全局":
            if CURRENT_SETTINGS["settings"]["mode"] == "现有环境":
                path = CURRENT_SETTINGS["settings"]["custom_python_path"]
                if not path:
                    Message.error("错误", "请设置Python环境", self)
                    return
            elif CURRENT_SETTINGS["settings"]["mode"] == "Pyenv 环境":
                if not CURRENT_SETTINGS["settings"]["pyenv_current_version"]:
                    Message.error("错误", "请设置Pyenv环境", self)
                    return
                path = os.path.join(LIBS["pyenv"], "versions", CURRENT_SETTINGS["settings"]["pyenv_current_version"], "python.exe")
            else:
                pass
        elif self.comboBox_mode.currentText() == "跟随项目":
            pass
        return path

    def open_pyinstaller(self):
        if not self.button_filepath_main.text() or self.button_filepath_main.text() == "选择":
            Message.error("错误", "请选择程序入口", self)
            return

        if not os.path.exists(os.path.join(ROOT_PATH, SettingPath, "pyinstaller.json")):
            Message.error("错误", "配置文件不存在", self)
            return

        path = self.getPyPath()
        if not path:
            Message.error("错误", "python解释器获取失败", self)
            return


        with open(os.path.join(ROOT_PATH, SettingPath, "pyinstaller.json"), "r") as f:
            try:
                data = json.load(f)
            except:
                Message.error("错误", "配置文件格式错误", self)
                return
            PyinstallerPackage.PYINSTALLER_PARAMS.clear()
            for key in data.keys():
                PyinstallerPackage.PYINSTALLER_PARAMS[key] = data[key]



        file = self.button_filepath_main.text()
        (filepath, filename) = os.path.split(file)
        (name, suffix) = os.path.splitext(filename)
        if self.button_filepath_out.text():
            PyinstallerPackage.PYINSTALLER_PARAMS["distpath"] = self.button_filepath_out.text()
        else:
            PyinstallerPackage.PYINSTALLER_PARAMS["distpath"] = filepath
        now = datetime.datetime.now().strftime("%Y%m%d%H%M")
        PyinstallerPackage.PYINSTALLER_PARAMS["outName"] = name

        tmp = PyinstallerPackage.PYINSTALLER_PARAMS["iconPath"]
        if not Path(tmp).is_absolute():
            PyinstallerPackage.PYINSTALLER_PARAMS["iconPath"] = os.path.join(filepath, tmp)

        cmd = PyPath.PYINSTALLER.path(path) + ' ' + PyinstallerPackage().getCMD() + " " + file

        PyinstallerPackage.PYINSTALLER_PARAMS["iconPath"] = tmp

        cmd1 = "move " + os.path.join(PyinstallerPackage.PYINSTALLER_PARAMS["distpath"], name + ".exe") + " " + os.path.join(PyinstallerPackage.PYINSTALLER_PARAMS["distpath"], name + "_" + now + ".exe")

        self.venvMangerTh.setPyInterpreter(path)
        self.venvMangerTh.setCMD("pack_pyinstaller", cmd, cmd1)
        self.venvMangerTh.start()

        self.button_open.setEnabled(False)
        self.spinner_open.setState(True)
        self.spinner_open.show()

        Message.info("提示", "打包中，请稍后", self)

    def open_nuitka(self):
        if self.venvMangerTh.isRunning():
            Message.error("错误", "env忙碌中，请稍后重试", self)
            return

        if not self.button_filepath_main.text() or self.button_filepath_main.text() == "选择":
            Message.error("错误", "请选择程序入口", self)
            return

        if not os.path.exists(os.path.join(ROOT_PATH, SettingPath, "pyinstaller.json")):
            Message.error("错误", "配置文件不存在", self)
            return

        path = self.getPyPath()
        if not path:
            Message.error("错误", "python解释器获取失败", self)
            return

        with open(os.path.join(ROOT_PATH, SettingPath, "nuitka.json"), "r") as f:
            try:
                data = json.load(f)
            except:
                Message.error("错误", "配置文件格式错误", self)
                return
            NuitkaPackage.NUITKA_PARAMS.clear()
            for key in data.keys():
                NuitkaPackage.NUITKA_PARAMS[key] = data[key]

        file = self.button_filepath_main.text()
        (filepath, filename) = os.path.split(file)
        PyinstallerPackage.PYINSTALLER_PARAMS["distpath"] = filepath

        cmd = ''


        self.venvMangerTh.setPyInterpreter(path)
        self.venvMangerTh.setCMD("pack_pyinstaller", cmd)
        self.venvMangerTh.start()

        self.button_open.setEnabled(False)
        self.spinner_open.setState(True)
        self.spinner_open.show()

        Message.info("提示", "打包中，请稍后", self)

    def pyinstaller_install(self):
        if self.pyinstaller("pyinstaller_install", "pyinstaller"):
            Message.info("提示", "安装中，请稍后", self)

    def pyinstaller_upgrade(self):
        if self.pyinstaller("pyinstaller_upgrade", "pyinstaller"):
            Message.info("提示", "更新中，请稍后", self)

    def pyinstaller_uninstall(self):
        if self.pyinstaller("pyinstaller_uninstall", "pyinstaller"):
            Message.info("提示", "卸载中，请稍后", self)

    def pyinstaller(self, cmd, args):
        if self.venvMangerTh.isRunning():
            Message.error("错误", "env忙碌中，请稍后重试", self)
            return False

        path = self.getPyPath()
        if not path:
            Message.error("错误", "python解释器获取失败", self)
            return False

        self.venvMangerTh.setPyInterpreter(path)
        self.venvMangerTh.setCMD(cmd, args)
        self.venvMangerTh.start()

        self.button_pyinstaller.setEnabled(False)
        self.spinner_pyinstaller.setState(True)
        self.spinner_pyinstaller.show()

        return True

    def nuitka_install(self):
        if self.nuitka("nuitka_install", "nuitka"):
            Message.info("提示", "安装中，请稍后", self)

    def nuitka_upgrade(self):
        if self.nuitka("nuitka_upgrade", "nuitka"):
            Message.info("提示", "更新中，请稍后", self)

    def nuitka_uninstall(self):
        if self.nuitka("nuitka_uninstall", "nuitka"):
            Message.info("提示", "卸载中，请稍后", self)

    def nuitka(self, cmd, args):
        if self.venvMangerTh.isRunning():
            Message.error("错误", "env忙碌中，请稍后重试", self)
            return False

        path = self.getPyPath()
        if not path:
            Message.error("错误", "python解释器获取失败", self)
            return False

        self.venvMangerTh.setPyInterpreter(path)
        self.venvMangerTh.setCMD(cmd, args)
        self.venvMangerTh.start()

        self.button_nuitka.setEnabled(False)
        self.spinner_nuitka.setState(True)
        self.spinner_nuitka.show()

        return True

    def on_comboBox_mode_currentTextChanged(self, text):
        CURRENT_SETTINGS["pack"]["mode"] = text

        if text == "跟随项目":
            self.widget_env.hide()
        elif text == "跟随全局":
            self.widget_env.hide()
        elif text == "独立模式":
            self.widget_env.show()
        else:
            pass

        write_config()

    def on_button_filepath_textChanged(self, text):
        if text:
            self.venvMangerTh.setPyInterpreter(text)
            self.venvMangerTh.setCMD("py_version")
            self.venvMangerTh.start()
        else:
            self.label_ver.setText("版本: ")
            CURRENT_SETTINGS["pack"]["custom_python_path"] = ""
            write_config()

    def on_button_filepath_main_textChanged(self, text):
        if text:
            CURRENT_SETTINGS["pack"]["main"] = text
            write_config()

    def on_button_filepath_out_textChanged(self, text):
        if text:
            CURRENT_SETTINGS["pack"]["outPath"] = text
            write_config()

    def on_button_pyinstaller_settingfile_clicked(self):
        if not os.path.exists(os.path.join(ROOT_PATH, SettingPath, "pyinstaller.json")):
            Message.error("错误", "配置文件不存在", self)
            return
        os.system(f'notepad {os.path.join(ROOT_PATH, SettingPath, "pyinstaller.json")}')

    def on_button_nuitka_settingfile_clicked(self):
        if not os.path.exists(os.path.join(ROOT_PATH, SettingPath, "nuitka.json")):
            Message.error("错误", "配置文件不存在", self)
            return
        os.system(f'notepad {os.path.join(ROOT_PATH, SettingPath, "nuitka.json")}')

    def receive_VMresult(self, cmd, result):
        if cmd == "init":
            pass
        elif cmd == "py_version":
            self.label_ver.setText("版本: " + result[1])
            CURRENT_SETTINGS["pack"]["custom_python_path"] = self.button_filepath.text()
            write_config()
        elif cmd == "pyinstaller_install":
            self.button_pyinstaller.setEnabled(True)
            self.spinner_pyinstaller.setState(False)
            self.spinner_pyinstaller.hide()

            if not result[0]:
                Message.error("错误", result[1], self)
                return

            Message.info("成功", "安装成功", self)
        elif cmd == "pyinstaller_upgrade":
            self.button_pyinstaller.setEnabled(True)
            self.spinner_pyinstaller.setState(False)
            self.spinner_pyinstaller.hide()

            if not result[0]:
                Message.error("错误", result[1], self)
                return

            Message.info("成功", "更新成功", self)
        elif cmd == "pyinstaller_uninstall":
            self.button_pyinstaller.setEnabled(True)
            self.spinner_pyinstaller.setState(False)
            self.spinner_pyinstaller.hide()

            if not result[0]:
                Message.error("错误", result[1], self)
                return

            Message.info("成功", "卸载成功", self)
        elif cmd == "nuitka_install":
            self.button_nuitka.setEnabled(True)
            self.spinner_nuitka.setState(False)
            self.spinner_nuitka.hide()

            if not result[0]:
                Message.error("错误", result[1], self)
                return

            Message.info("成功", "安装成功", self)
        elif cmd == "nuitka_upgrade":
            self.button_nuitka.setEnabled(True)
            self.spinner_nuitka.setState(False)
            self.spinner_nuitka.hide()

            if not result[0]:
                Message.error("错误", result[1], self)
                return

            Message.info("成功", "更新成功", self)
        elif cmd == "nuitka_uninstall":
            self.button_nuitka.setEnabled(True)
            self.spinner_nuitka.setState(False)
            self.spinner_nuitka.hide()

            if not result[0]:
                Message.error("错误", result[1], self)
                return

            Message.info("成功", "卸载成功", self)
        elif cmd == "pack_pyinstaller" or cmd == "pack_nuitka":
            self.button_open.setEnabled(True)
            self.spinner_open.setState(False)
            self.spinner_open.hide()

            if not result[0]:
                Message.error("错误", result[1], self)
                return

            Message.info("成功", "打包成功", self)
        else:
            pass


class VenvManagerThread(QThread):

    signal_result = Signal(str, tuple)

    def __init__(self, parent=None):
        super().__init__(parent)
        # self.venvManger = PyVenvManager(LIBS["pyenv"])
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
        if self.cmd == "init":
            pass
        elif self.cmd == "environ":
            self.pyI.setEnviron(**self.kwargs)
        elif self.cmd == "py_version":
            result = self.pyI.version()
            self.signal_result.emit(self.cmd, result)
        elif self.cmd == "pyinstaller_install":
            result = self.pyI.pip("install", *self.args)
            self.signal_result.emit(self.cmd, result)
        elif self.cmd == "pyinstaller_upgrade":
            result = self.pyI.pip("install", "--upgrade", *self.args)
            self.signal_result.emit(self.cmd, result)
        elif self.cmd == "pyinstaller_uninstall":
            result = self.pyI.pip("uninstall", '-y', *self.args)
            self.signal_result.emit(self.cmd, result)
        elif self.cmd == "nuitka_install":
            result = self.pyI.pip("install", *self.args)
            self.signal_result.emit(self.cmd, result)
        elif self.cmd == "nuitka_upgrade":
            result = self.pyI.pip("install", "--upgrade", *self.args)
            self.signal_result.emit(self.cmd, result)
        elif self.cmd == "nuitka_uninstall":
            result = self.pyI.pip("uninstall", '-y', *self.args)
            self.signal_result.emit(self.cmd, result)
        elif self.cmd == "pack_pyinstaller":
            result = self.pyI.cmd(self.args[0])
            if result[0]:
                result = self.pyI.cmd(self.args[1])
            else:
                self.signal_result.emit(self.cmd, result)
                return
            self.signal_result.emit(self.cmd, result)
        elif self.cmd == "pack_nuitka":
            result = self.pyI.pip(*self.args)
            self.signal_result.emit(self.cmd, result)
        else:
            self.signal_result.emit(self.cmd, ["False", "未知命令"])