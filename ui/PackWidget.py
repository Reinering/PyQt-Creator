#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author: Reiner New
email: nbxlc@hotmail.com
Module implementing PackWidget.
"""


from PySide6.QtCore import Slot, QRect, Qt, QThread, Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget, QGridLayout, QHBoxLayout, QVBoxLayout, QSpacerItem, QSizePolicy, QMessageBox
import os
import datetime, time
import simplejson as json
from pathlib import Path
import logging

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
from qfluentexpand.components.line.editor import Line
from qfluentexpand.components.label.label import GifLabel
from qfluentexpand.common.gif import APPGIF
from qfluentexpand.components.widgets.card import (
    SettingCardWidget, ComboBoxSettingCardWidget, FileSettingCardWidget, FolderSettingCardWidget,
    LineSettingCardWidget, PrimaryPushSettingCardWidget
)

from .Ui_PackWidget import Ui_Form
from .utils.stylesheets import StyleSheet
from .utils.config import write_config
from .utils.tool import startCMD
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
        self.spinner_open.setGif(APPGIF.LOADING)
        self.spinner_open.setFixedSize(30, 30)
        self.spinner_open.hide()
        self.button_open = PrimaryDropDownPushButton(FluentIcon.BRUSH, '打包')
        menu = RoundMenu(parent=self.button_open)
        menu.addAction(Action(FluentIcon.CERTIFICATE, 'pyinstaller', triggered=self.open_pyinstaller))
        menu.addAction(Action(FluentIcon.FLAG, 'nuitka', triggered=self.open_nuitka))
        menu.addAction(Action(FluentIcon.ROTATE, 'build', triggered=self.open_setup))
        menu.addAction(Action(FluentIcon.CLOSE, '停止', triggered=self.open_stop))
        self.button_open.setMenu(menu)

        layout.addItem(horizontalSpacer)
        layout.addWidget(self.spinner_open)
        layout.addWidget(self.button_open)
        hBoxLayout.addLayout(layout, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

    def initWidget(self):
        self.envCard = SettingGroupCard(FluentIcon.SETTING, "环境设置", "",
                                        self.scrollAreaWidgetContents)
        self.gridLayout1.addWidget(self.envCard, 1, 0, 1, 1)

        self.comboBox_mode = ComboBoxSettingCardWidget('', '模式', '', self.envCard)
        self.comboBox_mode.addItems(SETTINGS["designer"]["python_env_modes"])
        self.comboBox_mode.currentTextChanged.connect(self.on_comboBox_mode_currentTextChanged)
        self.envCard.addWidget(self.comboBox_mode)

        self.widget_env = SettingCardWidget('', 'Python 环境', '', self.envCard)
        self.label_ver = CaptionLabel("版本: ", self.envCard)
        self.button_filepath = FilePathSelector(self.envCard)
        self.button_filepath.setFileTypes("python.exe")
        self.button_filepath.setFixedWidth(200)
        self.button_filepath.textChanged.connect(self.on_button_filepath_textChanged)
        self.widget_env.addWidget(self.label_ver)
        self.widget_env.addStretch(1)
        self.widget_env.addWidget(self.button_filepath)
        self.envCard.addWidget(self.widget_env)

        self.widget_teminal = SettingCardWidget('', '命令行窗口', 'cmd', self.envCard)
        self.button_teminal = PrimaryPushButton(FluentIcon.UP, "打开")
        self.button_teminal.clicked.connect(self.on_button_teminal_clicked)
        self.widget_teminal.addStretch(1)
        self.widget_teminal.addWidget(self.button_teminal)
        self.envCard.addWidget(self.widget_teminal)

        self.button_filepath_main = FileSettingCardWidget('', "程序入口", "", self.envCard)
        self.button_filepath_main.setFileTypes("python(*.py)")
        self.button_filepath_main.selector.setReadOnly(False)
        self.button_filepath_main.selector.setMinimumWidth(300)
        self.button_filepath_main.textChanged.connect(self.on_button_filepath_main_textChanged)
        self.envCard.addWidget(self.button_filepath_main)

        self.button_filepath_out = FolderSettingCardWidget('', "输出目录", "", self.envCard)
        self.button_filepath_out.selector.setPlaceholderText("默认为程序入口目录")
        self.button_filepath_out.selector.setFixedWidth(300)
        self.button_filepath_out.textChanged.connect(self.on_button_filepath_out_textChanged)
        self.envCard.addWidget(self.button_filepath_out)

        self.button_filename_out = LineSettingCardWidget('', "输出文件名", "", self.envCard)
        self.button_filename_out.line.setPlaceholderText("默认与程序入口文件名一致")
        self.button_filename_out.line.setFixedWidth(300)
        self.button_filename_out.line.setClearButtonEnabled(True)
        self.button_filename_out.textChanged.connect(self.on_button_filename_out_textChanged)
        self.envCard.addWidget(self.button_filename_out)

        self.card_pyinstaller = SettingGroupCard(FluentIcon.SETTING, "Pyinstaller 设置", "参考文档配置参数",
                                                 self.scrollAreaWidgetContents)
        self.gridLayout1.addWidget(self.card_pyinstaller, 2, 0, 1, 1)

        widget_pyinstaller = SettingCardWidget('', 'Pyinstaller 模块', '', self.card_pyinstaller)
        self.spinner_pyinstaller = GifLabel(self.card_pyinstaller)
        self.spinner_pyinstaller.setGif(APPGIF.LOADING)
        self.spinner_pyinstaller.setFixedSize(30, 30)
        self.spinner_pyinstaller.hide()
        self.button_pyinstaller = PrimaryDropDownPushButton(FluentIcon.ADD_TO, '操作')
        menu = RoundMenu(parent=self.button_pyinstaller)
        menu.addAction(Action(FluentIcon.PRINT, '安装', triggered=self.pyinstaller_install))
        menu.addAction(Action(FluentIcon.UPDATE, '更新', triggered=self.pyinstaller_upgrade))
        menu.addAction(Action(FluentIcon.ROBOT, '卸载', triggered=self.pyinstaller_uninstall))
        self.button_pyinstaller.setMenu(menu)
        widget_pyinstaller.addStretch(1)
        widget_pyinstaller.addWidget(self.spinner_pyinstaller)
        widget_pyinstaller.addWidget(self.button_pyinstaller)
        self.card_pyinstaller.addWidget(widget_pyinstaller)

        self.button_pyinstaller_settingfile = PrimaryPushSettingCardWidget('', 'pyinstaller 配置文件', '', self.card_pyinstaller)
        self.button_pyinstaller_settingfile.setButtonText("编辑")
        self.button_pyinstaller_settingfile.clicked.connect(self.on_button_pyinstaller_settingfile_clicked)
        self.card_pyinstaller.addWidget(self.button_pyinstaller_settingfile)

        self.card_nuitka = SettingGroupCard(FluentIcon.SETTING, "Nuitka 设置", "参考文档配置参数",
                                                self.scrollAreaWidgetContents)
        self.gridLayout1.addWidget(self.card_nuitka, 3, 0, 1, 1)

        widget_nuitka = SettingCardWidget('', 'Nuitka 模块', '', self.card_nuitka)
        self.spinner_nuitka = GifLabel(self.card_nuitka)
        self.spinner_nuitka.setGif(APPGIF.LOADING)
        self.spinner_nuitka.setFixedSize(30, 30)
        self.spinner_nuitka.hide()
        self.button_nuitka = PrimaryDropDownPushButton(FluentIcon.ADD_TO, '操作')
        menu = RoundMenu(parent=self.button_nuitka)
        menu.addAction(Action(FluentIcon.PRINT, '安装', triggered=self.nuitka_install))
        menu.addAction(Action(FluentIcon.UPDATE, '更新', triggered=self.nuitka_upgrade))
        menu.addAction(Action(FluentIcon.ROBOT, '卸载', triggered=self.nuitka_uninstall))
        self.button_nuitka.setMenu(menu)
        widget_nuitka.addStretch(1)
        widget_nuitka.addWidget(self.spinner_nuitka)
        widget_nuitka.addWidget(self.button_nuitka)
        self.card_nuitka.addWidget(widget_nuitka)

        self.button_nuitka_settingfile = PrimaryPushSettingCardWidget('', 'nuitka 配置文件', '',
                                                                           self.card_nuitka)
        self.button_nuitka_settingfile.setButtonText("编辑")
        self.button_nuitka_settingfile.clicked.connect(self.on_button_nuitka_settingfile_clicked)
        self.card_nuitka.addWidget(self.button_nuitka_settingfile)

        self.card_setup = SettingGroupCard(FluentIcon.SETTING, "Setuptools 设置", "参考文档配置参数",
                                            self.scrollAreaWidgetContents)
        self.gridLayout1.addWidget(self.card_setup, 4, 0, 1, 1)

        widget_env_setuptools = SettingCardWidget('', 'setuptools 模块', '', self.card_setup)
        self.spinner_setuptools = GifLabel(self.card_setup)
        self.spinner_setuptools.setGif(APPGIF.LOADING)
        self.spinner_setuptools.setFixedSize(30, 30)
        self.spinner_setuptools.hide()
        self.button_setuptools = PrimaryPushButton(self.card_setup)
        self.button_setuptools.setText("安装/更新")
        self.button_setuptools.clicked.connect(self.on_button_setuptools_clicked)
        widget_env_setuptools.addStretch(1)
        widget_env_setuptools.addWidget(self.spinner_setuptools)
        widget_env_setuptools.addWidget(self.button_setuptools)
        self.card_setup.addWidget(widget_env_setuptools)

        widget_env_setup = SettingCardWidget('', 'setup.py', '', self.card_setup)
        self.spinner_setup_action = GifLabel(self.card_setup)
        self.spinner_setup_action.setGif(APPGIF.LOADING)
        self.spinner_setup_action.setFixedSize(30, 30)
        self.spinner_setup_action.hide()
        self.button_filepath_setup = FilePathSelector(self.card_setup)
        self.button_filepath_setup.setFileTypes("setup.py")
        self.button_filepath_setup.setFixedWidth(300)
        self.button_filepath_setup.textChanged.connect(self.on_button_filepath_setup_textChanged)
        self.button_setup_action = PrimaryDropDownPushButton(FluentIcon.ADD_TO, '操作')
        menu = RoundMenu(parent=self.button_setup_action)
        menu.addAction(Action(FluentIcon.EDIT, '编辑', triggered=self.setup_edit))
        menu.addAction(Action(FluentIcon.PRINT, '安装', triggered=self.setup_install))
        # menu.addAction(Action(FluentIcon.ALBUM, '更新', triggered=self.setup_upgrade))
        # menu.addAction(Action(FluentIcon.ALBUM, '卸载', triggered=self.setup_uninstall))
        self.button_setup_action.setMenu(menu)
        widget_env_setup.addStretch(1)
        widget_env_setup.addWidget(self.spinner_setup_action)
        widget_env_setup.addWidget(self.button_filepath_setup)
        widget_env_setup.addWidget(self.button_setup_action)
        self.card_setup.addWidget(widget_env_setup)

        verticalSpacer = QSpacerItem(0, 1000, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.gridLayout1.addItem(verticalSpacer, 5, 0, 1, 1)

        try:
            self.configure()
        except Exception as e:
            logging.error(e)
            QMessageBox.critical(self, "初始化错误", f"请检查配置文件{str(e)}")
            raise Exception(f"请检查配置文件{str(e)}")

    def configure(self):
        if CURRENT_SETTINGS["pack"]["mode"] in SETTINGS["pack"]["python_env_modes"]:
            self.comboBox_mode.setCurrentText(CURRENT_SETTINGS["pack"]["mode"])

        if CURRENT_SETTINGS["pack"]["custom_python_path"]:
            self.button_filepath.setText(CURRENT_SETTINGS["pack"]["custom_python_path"])

        if CURRENT_SETTINGS["pack"]["main"]:
            self.button_filepath_main.setText(CURRENT_SETTINGS["pack"]["main"])

        if CURRENT_SETTINGS["pack"]["outPath"]:
            self.button_filepath_out.setText(CURRENT_SETTINGS["pack"]["outPath"])

        if CURRENT_SETTINGS["pack"]["outName"]:
            self.button_filename_out.setText(CURRENT_SETTINGS["pack"]["outName"])

        if CURRENT_SETTINGS["pack"]["setup"]["filepath"]:
            self.button_filepath_setup.setText(CURRENT_SETTINGS["pack"]["setup"]["filepath"])

    def getPyPath(self):
        path = ""
        mode = self.comboBox_mode.currentText()
        if mode == "独立模式":
            path = self.button_filepath.text()
            if not path:
                Message.error("错误", "请选择Python环境", self)
                return
        elif mode == "跟随全局":
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
        elif mode == "跟随项目":
            if CURRENT_SETTINGS["project"]["mode"] == "独立模式":
                if not CURRENT_SETTINGS["project"]["custom_python_path"]:
                    Message.error("错误", "请设置Python环境", self)
                    return

                path = CURRENT_SETTINGS["project"]["custom_python_path"]
            elif CURRENT_SETTINGS["project"]["mode"] == "跟随全局":
                if CURRENT_SETTINGS["settings"]["mode"] == "现有环境":
                    path = CURRENT_SETTINGS["settings"]["custom_python_path"]
                    if not path:
                        Message.error("错误", "请设置Python环境", self)
                        return
                elif CURRENT_SETTINGS["settings"]["mode"] == "Pyenv 环境":
                    if not CURRENT_SETTINGS["settings"]["pyenv_current_version"]:
                        Message.error("错误", "请设置Pyenv环境", self)
                        return
                    path = os.path.join(LIBS["pyenv"], "versions",
                                        CURRENT_SETTINGS["settings"]["pyenv_current_version"], "python.exe")
                else:
                    pass

        return path

    def open_stop(self):
        if not self.venvMangerTh.isRunning():
            return

        self.venvMangerTh.stop()
        self.spinner_open.setState(False)
        self.spinner_open.hide()

        Message.info("提示", "线程已停止", self)

    def open_pyinstaller(self):
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
        if not Path(path).is_absolute():
            path = str(Path(path).absolute())

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
        if self.button_filename_out.text():
            name = self.button_filename_out.text()
        elif PyinstallerPackage.PYINSTALLER_PARAMS["outName"]:
            name = PyinstallerPackage.PYINSTALLER_PARAMS["outName"]
        else:
            (name, suffix) = os.path.splitext(filename)

        if self.button_filepath_out.text():
            PyinstallerPackage.PYINSTALLER_PARAMS["distpath"] = self.button_filepath_out.text()
        else:
            PyinstallerPackage.PYINSTALLER_PARAMS["distpath"] = filepath
        now = datetime.datetime.now().strftime("%Y%m%d%H%M")

        tmp = False
        if not NuitkaPackage.NUITKA_PARAMS["output-filename"]:
            PyinstallerPackage.PYINSTALLER_PARAMS["outName"] = name
            tmp = True


        # tmp = PyinstallerPackage.PYINSTALLER_PARAMS["iconPath"]
        # if not Path(tmp).is_absolute():
        #     PyinstallerPackage.PYINSTALLER_PARAMS["iconPath"] = os.path.join(filepath, tmp)

        (pypath, pyfilename) = os.path.split(path)

        pythonPath = []
        pythonPath.append(path)
        pythonPath.append(filepath)
        pythonPath.append(pypath)
        pythonPath.append(os.path.join(pypath, "python312.zip"))
        pythonPath.append(os.path.join(pypath, "DLLs"))
        pythonPath.append(os.path.join(pypath, "Lib"))
        pythonPath.append(os.path.join(pypath, "Lib", "site-packages"))
        pythonPath.append(os.path.join(pypath, "Lib", "site-packages", "win32"))
        pythonPath.append(os.path.join(pypath, "Lib", "site-packages", "win32", "lib"))
        pythonPath.append(os.path.join(pypath, "Lib", "site-packages", "Pythonwin"))

        try:
            cmd = "cd /d " + filepath + ' && ' + PyPath.PYINSTALLER.path(path) + ' ' + PyinstallerPackage().getCMD() + " " + filename
        except Exception as e:
            logging.error(e)
            Message.error("错误", str(e), self)
            return

        if PyinstallerPackage.PYINSTALLER_PARAMS["outType"] == "FILE":
            suffix = ".exe"
        else:
            suffix = ""

        if PyinstallerPackage.PYINSTALLER_PARAMS["console"]:
            cmd1 = "move " + os.path.join(PyinstallerPackage.PYINSTALLER_PARAMS["distpath"], name + suffix) + " " + os.path.join(PyinstallerPackage.PYINSTALLER_PARAMS["distpath"], name + "_Beta_" + now + suffix)
        else:
            cmd1 = "move " + os.path.join(PyinstallerPackage.PYINSTALLER_PARAMS["distpath"], name + suffix) + " " + os.path.join(PyinstallerPackage.PYINSTALLER_PARAMS["distpath"], name + "_" + now + suffix)

        if tmp:
            PyinstallerPackage.PYINSTALLER_PARAMS["outName"] = ''

        self.venvMangerTh.setPyInterpreter(path)
        self.venvMangerTh.setEnviron(PYTHONPATH=(';').join(pythonPath))
        self.venvMangerTh.setCMD("pack_pyinstaller", cmd, cmd1)
        self.venvMangerTh.start()

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
        if not Path(path).is_absolute():
            path = str(Path(path).absolute())

        with open(os.path.join(ROOT_PATH, SettingPath, "nuitka.json"), "r") as f:
            try:
                data = json.load(f)
            except:
                Message.error("错误", "配置文件格式错误", self)
                return
            NuitkaPackage.NUITKA_PARAMS.clear()
            for key in data.keys():
                NuitkaPackage.NUITKA_PARAMS[key] = data[key]

        now = datetime.datetime.now().strftime("%Y%m%d%H%M")
        file = self.button_filepath_main.text()
        (filepath, filename) = os.path.split(file)
        (name1, suffix) = os.path.splitext(filename)
        if self.button_filename_out.text():
            name = self.button_filename_out.text()
            # NuitkaPackage.NUITKA_PARAMS["output-filename"] = self.button_filename_out.text()
        elif NuitkaPackage.NUITKA_PARAMS["output-filename"]:
            name = NuitkaPackage.NUITKA_PARAMS["output-filename"]
        else:
            name = name1

        # if not NuitkaPackage.NUITKA_PARAMS["main"]:
        #     NuitkaPackage.NUITKA_PARAMS["main"] = file

        if self.button_filepath_out.text():
            NuitkaPackage.NUITKA_PARAMS["output-dir"] = self.button_filepath_out.text()
        else:
            NuitkaPackage.NUITKA_PARAMS["output-dir"] = filepath

        tmp = False
        if not NuitkaPackage.NUITKA_PARAMS["output-filename"]:
            NuitkaPackage.NUITKA_PARAMS["output-filename"] = name
            tmp = True

        (pypath, pyfilename) = os.path.split(path)

        pythonPath = []
        pythonPath.append(path)
        pythonPath.append(filepath)
        pythonPath.append(pypath)
        pythonPath.append(os.path.join(pypath, "python312.zip"))
        pythonPath.append(os.path.join(pypath, "DLLs"))
        pythonPath.append(os.path.join(pypath, "Lib"))
        pythonPath.append(os.path.join(pypath, "Lib", "site-packages"))
        pythonPath.append(os.path.join(pypath, "Lib", "site-packages", "win32"))
        pythonPath.append(os.path.join(pypath, "Lib", "site-packages", "win32", "lib"))
        pythonPath.append(os.path.join(pypath, "Lib", "site-packages", "Pythonwin"))

        try:
            cmd = "cd /d " + filepath + ' && ' + path + " -m nuitka " + NuitkaPackage().getCMD() + ' ' + file
        except Exception as e:
            logging.error(e)
            Message.error("错误", str(e), self)
            return

        if NuitkaPackage.NUITKA_PARAMS["onefile"]:
            name = NuitkaPackage.NUITKA_PARAMS["output-filename"]
            suffix = ".exe"
            if NuitkaPackage.NUITKA_PARAMS["windows-console-mode"] != "disable":
                cmd1 = "move " + os.path.join(NuitkaPackage.NUITKA_PARAMS["output-dir"],
                                              name + suffix) + " " + os.path.join(
                    NuitkaPackage.NUITKA_PARAMS["output-dir"], name + "_Beta_" + now + suffix)
            else:
                cmd1 = "move " + os.path.join(NuitkaPackage.NUITKA_PARAMS["output-dir"],
                                              name + suffix) + " " + os.path.join(
                    NuitkaPackage.NUITKA_PARAMS["output-dir"], name+ "_" + now + suffix)
        else:
            name = NuitkaPackage.NUITKA_PARAMS["output-filename"]
            if NuitkaPackage.NUITKA_PARAMS["windows-console-mode"] != "disable":
                cmd1 = "move " + os.path.join(NuitkaPackage.NUITKA_PARAMS["output-dir"],
                                          name1 + ".dist") + " " + os.path.join(
                NuitkaPackage.NUITKA_PARAMS["output-dir"],  name + "_Beta_" + now)
            else:
                cmd1 = "move " + os.path.join(NuitkaPackage.NUITKA_PARAMS["output-dir"],
                                          name1 + ".dist") + " " + os.path.join(
                NuitkaPackage.NUITKA_PARAMS["output-dir"], name + "_" + now)

        if tmp:
            NuitkaPackage.NUITKA_PARAMS["output-filename"] = ''

        self.venvMangerTh.setPyInterpreter(path)
        self.venvMangerTh.setEnviron(PYTHONPATH=(';').join(pythonPath))
        self.venvMangerTh.setCMD("pack_nuitka", cmd, cmd1)
        self.venvMangerTh.start()

        self.spinner_open.setState(True)
        self.spinner_open.show()

        Message.info("提示", "打包中，请稍后", self)

    def open_setup(self):
        if self.venvMangerTh.isRunning():
            Message.error("错误", "env忙碌中，请稍后重试", self)
            return

        file = self.button_filepath_setup.text()
        if not file or file == "选择":
            Message.error("错误", "请选择setup.py", self)
            return

        path = self.getPyPath()
        if not path:
            Message.error("错误", "python解释器获取失败", self)
            return
        if not Path(path).is_absolute():
            path = str(Path(path).absolute())

        file = self.button_filepath_setup.text()
        (filepath, filename) = os.path.split(file)

        cmd = "cd /d " + filepath + '&&' + f" {path} {filename} build " + '&&' + f" {path} {filename} sdist " + '&&' + f" {path} {filename} bdist_wheel"

        self.venvMangerTh.setPyInterpreter(path)
        self.venvMangerTh.setCMD("pack_setup", cmd)
        self.venvMangerTh.start()

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

    def setMainFile(self, file):
        self.comboBox_mode.setCurrentText(SETTINGS["pack"]["python_env_modes"][1])
        self.button_filepath_main.setText(file)

    def setSetupFile(self, file):
        if file == "setup.py":
            self.comboBox_mode.setCurrentText(SETTINGS["pack"]["python_env_modes"][1])
            self.button_filepath_setup.setText(file)

    def on_comboBox_mode_currentTextChanged(self, text):
        CURRENT_SETTINGS["pack"]["mode"] = text

        if text == "跟随项目":
            self.widget_env.hide()
            # self.widget_env_main.hide()
        elif text == "跟随全局":
            self.widget_env.hide()
            # self.widget_env_main.show()
        elif text == "独立模式":
            self.widget_env.show()
            # self.widget_env_main.show()
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
            CURRENT_SETTINGS["pack"]["custom_python_path"] = ""
            write_config()

    def on_button_teminal_clicked(self):
        path = self.getPyPath()
        if not path:
            Message.error("错误", "python解释器获取失败", self)
            return
        if not Path(path).is_absolute():
            path = str(Path(path).absolute())

        startCMD(path)

    def on_button_filepath_main_textChanged(self, text):
        if text:
            CURRENT_SETTINGS["pack"]["main"] = text
            write_config()

    def on_button_filepath_out_textChanged(self, text):
        if text:
            CURRENT_SETTINGS["pack"]["outPath"] = text
            write_config()

    def on_button_filename_out_textChanged(self, text):
        if text:
            CURRENT_SETTINGS["pack"]["outName"] = text
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

    def on_button_setuptools_clicked(self):
        if self.venvMangerTh.isRunning():
            Message.error("错误", "env忙碌中，请稍后重试", self)
            return

        path = self.getPyPath()
        if not path:
            Message.error("错误", "python解释器获取失败", self)
            return
        if not Path(path).is_absolute():
            path = str(Path(path).absolute())

        self.venvMangerTh.setPyInterpreter(path)
        self.venvMangerTh.setCMD("setuptools_install", "setuptools")
        self.venvMangerTh.start()

        self.button_setup_action.setEnabled(False)
        self.spinner_setup_action.setState(True)
        self.spinner_setup_action.show()

        Message.info("提示", "打包中，请稍后", self)

    def on_button_filepath_setup_textChanged(self, text):
        if text:
            CURRENT_SETTINGS["pack"]["setup"]["filepath"] = text
            write_config()

    def setup_edit(self):
        if not os.path.exists(self.button_filepath_setup.text()):
            Message.error("错误", "文件不存在", self)
            return
        os.system(f'notepad {self.button_filepath_setup.text()}')

    def setup_install(self):
        file = self.button_filepath_setup.text()
        if not os.path.exists(file):
            Message.error("错误", "文件不存在", self)
            return

        if self.venvMangerTh.isRunning():
            Message.error("错误", "env忙碌中，请稍后重试", self)
            return

        path = self.getPyPath()
        if not path:
            Message.error("错误", "python解释器获取失败", self)
            return
        if not Path(path).is_absolute():
            path = str(Path(path).absolute())

        file = self.button_filepath_setup.text()
        (filepath, filename) = os.path.split(file)

        cmd = "cd /d " + filepath + '&&' + f" {path} {filename} install "

        self.venvMangerTh.setPyInterpreter(path)
        self.venvMangerTh.setCMD("setup_install", cmd)
        self.venvMangerTh.start()

        self.button_setup_action.setEnabled(False)
        self.spinner_setup_action.setState(True)
        self.spinner_setup_action.show()

        Message.info("提示", "打包中，请稍后", self)

    def setup_upgrade(self):
        if not os.path.exists(self.button_filepath_setup.text()):
            Message.error("错误", "文件不存在", self)
            return

    def setup_uninstall(self):
        if not os.path.exists(self.button_filepath_setup.text()):
            Message.error("错误", "文件不存在", self)
            return

    def receive_VMresult(self, cmd, result):
        logging.debug(f"receive_VMresult: {cmd}, {result[1]}")
        if isinstance(result[1], list) and len(result[1]) > 5:
            output = result[1][-5:]
        else:
            output = result[1]

        if cmd == "init":
            pass
        elif cmd == "py_version":
            if not result[0]:
                Message.error("解释器错误", output, self)
                return
            self.label_ver.setText("版本: " + result[1].strip('\n'))
            CURRENT_SETTINGS["pack"]["custom_python_path"] = self.button_filepath.text()
            write_config()
        elif cmd == "pyinstaller_install":
            self.button_pyinstaller.setEnabled(True)
            self.spinner_pyinstaller.setState(False)
            self.spinner_pyinstaller.hide()

            if not result[0]:
                Message.error("错误", output, self)
                return

            Message.info("成功", "安装成功", self)
        elif cmd == "pyinstaller_upgrade":
            self.button_pyinstaller.setEnabled(True)
            self.spinner_pyinstaller.setState(False)
            self.spinner_pyinstaller.hide()

            if not result[0]:
                Message.error("错误", output, self)
                return

            Message.info("成功", "更新成功", self)
        elif cmd == "pyinstaller_uninstall":
            self.button_pyinstaller.setEnabled(True)
            self.spinner_pyinstaller.setState(False)
            self.spinner_pyinstaller.hide()

            if not result[0]:
                Message.error("错误", output, self)
                return

            Message.info("成功", "卸载成功", self)
        elif cmd == "nuitka_install":
            self.button_nuitka.setEnabled(True)
            self.spinner_nuitka.setState(False)
            self.spinner_nuitka.hide()

            if not result[0]:
                Message.error("错误", output, self)
                return

            Message.info("成功", "安装成功", self)
        elif cmd == "nuitka_upgrade":
            self.button_nuitka.setEnabled(True)
            self.spinner_nuitka.setState(False)
            self.spinner_nuitka.hide()

            if not result[0]:
                Message.error("错误", output, self)
                return

            Message.info("成功", "更新成功", self)
        elif cmd == "nuitka_uninstall":
            self.button_nuitka.setEnabled(True)
            self.spinner_nuitka.setState(False)
            self.spinner_nuitka.hide()

            if not result[0]:
                Message.error("错误", output, self)
                return

            Message.info("成功", "卸载成功", self)
        elif cmd == "pack_pyinstaller" or cmd == "pack_nuitka":
            self.spinner_open.setState(False)
            self.spinner_open.setState(True)
            self.spinner_open.hide()

            if not result[0]:
                Message.error("错误", "打包失败，详情请查看日志", self)
                return

            if result[-1]:
                minutes, seconds = divmod(int(result[-1]), 60)
                Message.info("成功", f"打包成功, 耗时：{minutes}分钟 {seconds}秒", self, duration=30000)
                logging.debug(f"receive_VMresult: {result[2]}")
            else:
                Message.info("成功", f"打包成功", self)
        elif cmd == "pack_setup":
            self.spinner_open.setState(False)
            self.spinner_open.setState(True)
            self.spinner_open.hide()

            if not result[0]:
                Message.error("错误", output, self)
                return

            Message.info("成功", "build成功", self)
        elif cmd == "setuptools_install":
            self.button_setuptools.setEnabled(True)
            self.spinner_setuptools.setState(False)
            self.spinner_setuptools.hide()

            if not result[0]:
                Message.error("错误", output, self)
                return

            Message.info("成功", "安装/更新 成功", self)
        elif cmd == "setup_install":
            self.button_setup_action.setEnabled(True)
            self.spinner_setup_action.setState(False)
            self.spinner_setup_action.hide()

            if not result[0]:
                Message.error("错误", output, self)
                return

            Message.info("成功", "安装/更新 成功", self)
        elif cmd == "setup_upgrade":
            pass
        elif cmd == "setup_uninstall":
            pass
        else:
            pass


class VenvManagerThread(QThread):

    signal_result = Signal(str, tuple)

    def __init__(self, parent=None):
        super().__init__(parent)
        # self.venvManger = PyVenvManager(LIBS["pyenv"])
        self.pyI = PyInterpreter()
        self.stopBool = False

    def stop(self):
        try:
            self.stopBool = True
            self.pyI.stop()
            self.terminate()
        except Exception as e:
            print(e)

    def setCMD(self, cmd, *args, **kwargs):
        self.cmd = cmd
        self.args = args
        self.kwargs = kwargs

    def setPyInterpreter(self, path):
        self.interpreter = path
        self.pyI.setInterpreter(path)

    def setEnviron(self, **kwargs):
        self.pyI.setEnviron(**kwargs)

    def run(self):
        cmd = self.cmd
        if cmd == "init":
            pass
        elif cmd == "environ":
            self.pyI.setEnviron(**self.kwargs)
        elif cmd == "py_version":
            result = self.pyI.version()
            self.signal_result.emit(cmd, result)
        elif cmd == "pyinstaller_install":
            result = self.pyI.pip("install", *self.args)
            self.signal_result.emit(cmd, result)
        elif cmd == "pyinstaller_upgrade":
            result = self.pyI.pip("install", "--upgrade", *self.args)
            self.signal_result.emit(cmd, result)
        elif cmd == "pyinstaller_uninstall":
            result = self.pyI.pip("uninstall", '-y', *self.args)
            self.signal_result.emit(cmd, result)
        elif cmd == "nuitka_install":
            result = self.pyI.pip("install", *self.args)
            self.signal_result.emit(cmd, result)
        elif cmd == "nuitka_upgrade":
            result = self.pyI.pip("install", "--upgrade", *self.args)
            self.signal_result.emit(cmd, result)
        elif cmd == "nuitka_uninstall":
            result = self.pyI.pip("uninstall", '-y', *self.args)
            self.signal_result.emit(cmd, result)
        elif cmd == "pack_pyinstaller":
            start = time.time()
            result = self.pyI.popen(self.args[0])
            if result[0]:
                self.pyI.cmd(self.args[1])
            else:
                self.signal_result.emit(cmd, result)
                return

            result.append(time.time() - start)
            self.signal_result.emit(cmd, result)
        elif cmd == "pack_nuitka":
            start = time.time()
            result = self.pyI.popen(self.args[0])
            if result[0]:
                self.pyI.cmd(self.args[1])
            else:
                self.signal_result.emit(cmd, result)
                return
            if len(result) > 50:
                result = result[-50:]
            result.append(time.time() - start)
            self.signal_result.emit(cmd, result)
        elif cmd == "pack_setup":
            result = self.pyI.popen(self.args[0])
            self.signal_result.emit(cmd, result)
        elif cmd == "setuptools_install":
            result = self.pyI.pip("install", "--upgrade", *self.args)
            self.signal_result.emit(cmd, result)
        elif cmd == "setup_install":
            result = self.pyI.popen(self.args[0])
            self.signal_result.emit(cmd, result)
        else:
            self.signal_result.emit(cmd, ["False", "未知命令"])