#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author: Reiner New
email: nbxlc@hotmail.com
Module implementing SettingWidget.
"""


from PySide6.QtCore import Slot, Qt, QThread, Signal
from PySide6.QtGui import QIcon, QFont
from PySide6.QtWidgets import QWidget, QGridLayout, QHBoxLayout, QVBoxLayout, QSpacerItem, QSizePolicy, QMessageBox
import os
from copy import copy
import logging
from pathlib import Path

from qfluentwidgets import (
    BodyLabel, CaptionLabel,
    ComboBox,
    PrimaryPushButton,  PrimaryDropDownPushButton, PrimaryDropDownToolButton,
    Theme, toggleTheme,
    LineEdit,
    RoundMenu, Action,
    PushSettingCard,
    FluentIcon
)

from qfluentexpand.components.widgets.card import (
    SettingCardWidget, PushSettingCardWidget, PrimaryPushSettingCardWidget, ComboBoxSettingCardWidget,
    FileSettingCardWidget, FolderSettingCardWidget, LineSettingCardWidget, HyperlinkCardWidget, SwitchSettingCardWidget
)
from qfluentexpand.components.combox.combo_box import MSComboBox, EditableComboBox
from qfluentexpand.components.card.settingcard import SettingGroupCard, FileSelectorSettingCard
from qfluentexpand.components.line.selector import FilePathSelector, FolderPathSelector
from qfluentexpand.components.label.label import GifLabel
from qfluentexpand.common.gif import APPGIF
from qfluentexpand.icongenie.icon import QFluentIcon

from .compoments.info import Message
from .Ui_SettingWidget import Ui_Form
from .utils.stylesheets import StyleSheet
from .utils.config import write_config
from .utils.tool import *
from common.pyenv import PyenvManager, PyenvVenvManager
from common.py import PyInterpreter, PyPath
from common.reg import *
from common.utils import is_admin
from manage import VERSION, PackageTime, LIBS, MIRRORS, SETTINGS, CURRENT_SETTINGS, BUNDLE_DIR


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
        StyleSheet.SETTING.apply(self)
        self.setObjectName("setting")

        self.initState = True

        self.gridLayout1 = QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout1.setObjectName(u"gridLayout")
        self.gridLayout1.setContentsMargins(50, -1, 50, -1)
        self.gridLayout1.setSpacing(20)
        self.gridLayout1.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.venvMangerTh = VenvManagerThread()
        self.venvMangerTh.signal_result.connect(self.receive_VMresult)

        self.initWidget()
        self.venvMangerTh.setPyenvPath(CURRENT_SETTINGS["settings"]["pyenv_path"])
        self.venvMangerTh.setPyenvVenvPath(CURRENT_SETTINGS["settings"]["pyenv_path"])
        self.venvMangerTh.setCMD("init")
        self.venvMangerTh.start()

    def initWidget(self):
        self.basicCard = SettingGroupCard(FluentIcon.SETTING, "基本设置", "",
                                          self.scrollAreaWidgetContents)
        self.gridLayout1.addWidget(self.basicCard, 1, 0, 1, 1)
        self.theme = SwitchSettingCardWidget(FluentIcon.FLAG, "主题", "theme", self.basicCard)
        self.theme.setOffText("Light")
        self.theme.setOnText("Dark")
        # self.theme.switch.checkedChanged.connect(self.on_theme_switch_checkedChanged)
        self.basicCard.addWidget(self.theme)


        self.envCard = SettingGroupCard(FluentIcon.SETTING, "环境设置", "",
                                        self.scrollAreaWidgetContents)
        self.gridLayout1.addWidget(self.envCard, 2, 0, 1, 1)

        self.comboBox_mode = ComboBoxSettingCardWidget('', '模式', '', self.envCard)
        self.comboBox_mode.addItems(SETTINGS["settings"]["python_env_modes"])
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
        self.button_teminal = PrimaryPushButton(QFluentIcon.googleIcon("Terminal"), "打开")
        self.button_teminal.clicked.connect(self.on_button_teminal_clicked)
        self.widget_teminal.addStretch(1)
        self.widget_teminal.addWidget(self.button_teminal)
        self.envCard.addWidget(self.widget_teminal)

        self.card_pyenv = SettingGroupCard(FluentIcon.SETTING, "Pyenv 虚拟环境管理", "https://github.com/pyenv-win/pyenv-win",
                                          self.scrollAreaWidgetContents)
        self.gridLayout1.addWidget(self.card_pyenv, 3, 0, 1, 1)

        self.button_pyenv_path = FolderSettingCardWidget('', "Pyenv 根目录", "pyenv-win", self.card_pyenv)
        self.button_pyenv_path.selector.setFixedWidth(200)
        self.button_pyenv_path.setReadOnly(False)
        # self.button_pyenv_path.textChanged.connect(self.on_button_pyenv_path_textChanged)
        self.button_pyenv_path.returnPressed.connect(self.on_button_pyenv_path_returnPressed)
        # self.button_pyenv_path_refresh = PrimaryPushButton(FluentIcon.UPDATE, "更新")
        # self.button_pyenv_path_refresh.clicked.connect(self.on_button_pyenv_path_refresh_clicked)
        # self.button_pyenv_path.addWidget(self.button_pyenv_path_refresh)
        self.card_pyenv.addWidget(self.button_pyenv_path)


        self.widget_pyenv_PATH = SettingCardWidget('', '添加全局环境变量', 'PATH: PYENV_HOME', self.card_pyenv)
        self.button_add_PATH = PrimaryPushButton(QFluentIcon.googleIcon("Terminal"), "添加")
        self.button_add_PATH.clicked.connect(self.on_button_add_PATH_clicked)
        self.widget_pyenv_PATH.addStretch(1)
        self.widget_pyenv_PATH.addWidget(self.button_add_PATH)
        self.card_pyenv.addWidget(self.widget_pyenv_PATH)


        self.widget_pyenv_existing = SettingCardWidget('', '现有环境', '', self.card_pyenv)
        self.spinner_existing = GifLabel(self.card_pyenv)
        self.spinner_existing.setGif(APPGIF.LOADING)
        self.spinner_existing.setFixedSize(30, 30)
        self.spinner_existing.hide()
        self.comboBox_existing = ComboBox(self.card_pyenv)
        self.comboBox_existing.setMinimumWidth(100)
        self.comboBox_existing.currentTextChanged.connect(self.on_comboBox_existing_currentTextChanged)

        self.button_existing_uninstall = PrimaryDropDownPushButton(FluentIcon.ADD_TO, '操作')
        menu = RoundMenu(parent=self.button_existing_uninstall)
        menu.addAction(Action(FluentIcon.SETTING, '设置Global', triggered=self.existing_setGlobal))
        menu.addAction(Action(FluentIcon.UPDATE, '更新', triggered=self.existing_update))
        menu.addAction(Action(FluentIcon.LINK, '卸载', triggered=self.existing_uninstall))
        self.button_existing_uninstall.setMenu(menu)
        self.widget_pyenv_existing.addStretch(1)
        self.widget_pyenv_existing.addWidget(self.spinner_existing)
        self.widget_pyenv_existing.addWidget(self.comboBox_existing)
        self.widget_pyenv_existing.addWidget(self.button_existing_uninstall)
        self.card_pyenv.addWidget(self.widget_pyenv_existing)

        self.widget_pyenv_global = SettingCardWidget('', 'Global', '', self.card_pyenv)
        self.lineEdit_global_ver = LineEdit(self.card_pyenv)
        self.lineEdit_global_ver.setEnabled(False)
        self.widget_pyenv_global.addStretch(1)
        self.widget_pyenv_global.addWidget(self.lineEdit_global_ver)
        self.card_pyenv.addWidget(self.widget_pyenv_global)

        self.widget_pyenv_new = SettingCardWidget('', '安装新环境', '', self.card_pyenv)
        self.spinner_new = GifLabel(self.card_pyenv)
        self.spinner_new.setGif(APPGIF.LOADING)
        self.spinner_new.setFixedSize(30, 30)
        self.spinner_new.hide()
        self.comboBox_new_maxbit = ComboBox(self.card_pyenv)
        self.comboBox_new_maxbit.addItems(SETTINGS["settings"]["pyenv_maxbit"])
        self.comboBox_new_maxbit.setFixedWidth(75)
        self.comboBox_new_ver = ComboBox(self.card_pyenv)
        self.comboBox_new_ver.setMinimumWidth(100)
        self.button_new_install = PrimaryDropDownPushButton(FluentIcon.ADD_TO, '操作')
        menu = RoundMenu(parent=self.button_new_install)
        menu.addAction(Action(FluentIcon.PRINT, '安装', triggered=self.new_install))
        menu.addAction(Action(FluentIcon.UPDATE, '更新', triggered=self.new_update))
        self.button_new_install.setMenu(menu)
        self.widget_pyenv_new.addStretch(1)
        self.widget_pyenv_new.addWidget(self.spinner_new)
        self.widget_pyenv_new.addWidget(self.comboBox_new_maxbit)
        self.widget_pyenv_new.addWidget(self.comboBox_new_ver)
        self.widget_pyenv_new.addWidget(self.button_new_install)
        self.card_pyenv.addWidget(self.widget_pyenv_new)

        self.widget_pyenv_mirror_url = ComboBoxSettingCardWidget('', '更新源', '', self.card_pyenv)
        self.widget_pyenv_mirror_url.comboBox.setMinimumWidth(100)
        self.widget_pyenv_mirror_url.comboBox.setMaximumWidth(150)
        self.widget_pyenv_mirror_url.addItems(MIRRORS["pyenv"].keys())
        self.widget_pyenv_mirror_url.currentTextChanged.connect(self.on_comboBox_pyenv_mirror_url_currentTextChanged)
        self.card_pyenv.addWidget(self.widget_pyenv_mirror_url)

        self.card_pyenv_venv = SettingGroupCard(FluentIcon.SETTING, "Pyenv-venv 虚拟环境管理",
                                           "https://github.com/pyenv-win/pyenv-win-venv",
                                           self.scrollAreaWidgetContents)
        self.gridLayout1.addWidget(self.card_pyenv_venv, 4, 0, 1, 1)

        self.widget_pyenv_venv_existing = SettingCardWidget('', '现有环境', '', self.card_pyenv_venv)
        self.spinner_venv_existing = GifLabel(self.card_pyenv_venv)
        self.spinner_venv_existing.setGif(APPGIF.LOADING)
        self.spinner_venv_existing.setFixedSize(30, 30)
        self.spinner_venv_existing.hide()
        self.comboBox_venv_existing = ComboBox(self.card_pyenv_venv)
        self.comboBox_venv_existing.setMinimumWidth(100)
        self.comboBox_venv_existing.currentTextChanged.connect(self.on_comboBox_venv_existing_currentTextChanged)

        self.button_venv_existing_uninstall = PrimaryDropDownPushButton(FluentIcon.ADD_TO, '操作')
        menu = RoundMenu(parent=self.button_venv_existing_uninstall)
        menu.addAction(Action(FluentIcon.UPDATE, '更新', triggered=self.venv_existing_refresh))
        menu.addAction(Action(FluentIcon.LINK, '卸载', triggered=self.venv_existing_uninstall))
        self.button_venv_existing_uninstall.setMenu(menu)
        self.widget_pyenv_venv_existing.addStretch(1)
        self.widget_pyenv_venv_existing.addWidget(self.spinner_venv_existing)
        self.widget_pyenv_venv_existing.addWidget(self.comboBox_venv_existing)
        self.widget_pyenv_venv_existing.addWidget(self.button_venv_existing_uninstall)
        self.card_pyenv_venv.addWidget(self.widget_pyenv_venv_existing)

        self.widget_pyenv_venv_install = SettingCardWidget('', '创建新环境', '基于Pyenv-win当前python版本', self.card_pyenv_venv)
        self.spinner_venv_install = GifLabel(self.card_pyenv_venv)
        self.spinner_venv_install.setGif(APPGIF.LOADING)
        self.spinner_venv_install.setFixedSize(30, 30)
        self.spinner_venv_install.hide()
        self.lineEdit_venv_install = LineEdit(self.card_pyenv_venv)
        self.button_venv_install = PrimaryPushButton(QFluentIcon.googleIcon("Terminal"), "创建")
        self.button_venv_install.clicked.connect(self.on_button_venv_install_clicked)
        self.widget_pyenv_venv_install.addStretch(1)
        self.widget_pyenv_venv_install.addWidget(self.spinner_venv_install)
        self.widget_pyenv_venv_install.addWidget(self.lineEdit_venv_install)
        self.widget_pyenv_venv_install.addWidget(self.button_venv_install)
        self.card_pyenv_venv.addWidget(self.widget_pyenv_venv_install)

        self.widget_pyenv_venv_teminal = SettingCardWidget('', '命令行窗口', 'cmd', self.envCard)
        self.button_venv_teminal = PrimaryPushButton(QFluentIcon.googleIcon("Terminal"), "激活并打开")
        self.button_venv_teminal.clicked.connect(self.on_button_venv_teminal_clicked)
        self.widget_pyenv_venv_teminal.addStretch(1)
        self.widget_pyenv_venv_teminal.addWidget(self.button_venv_teminal)
        self.card_pyenv_venv.addWidget(self.widget_pyenv_venv_teminal)





        self.card_pip = SettingGroupCard(FluentIcon.SETTING, "Pip 设置", "",
                                           self.scrollAreaWidgetContents)
        self.gridLayout1.addWidget(self.card_pip, 5, 0, 1, 1)

        self.widget_pip_mirror_url = ComboBoxSettingCardWidget('', '更新源', '', self.card_pip)
        self.widget_pip_mirror_url.comboBox.setMinimumWidth(100)
        self.widget_pip_mirror_url.comboBox.setMaximumWidth(150)
        self.widget_pip_mirror_url.addItems(MIRRORS["pip"].keys())
        self.widget_pip_mirror_url.currentTextChanged.connect(self.on_comboBox_pip_mirror_url_currentTextChanged)
        self.card_pip.addWidget(self.widget_pip_mirror_url)

        self.widget_pip_list = SettingCardWidget('', '模块列表', '', self.card_pip)
        self.spinner_pip_list = GifLabel(self.card_pip)
        self.spinner_pip_list.setGif(APPGIF.LOADING)
        self.spinner_pip_list.setFixedSize(30, 30)
        self.spinner_pip_list.hide()
        self.comboBox_pip_list = MSComboBox(self.card_pip)
        self.comboBox_pip_list.setMinimumWidth(150)
        self.comboBox_pip_list.setReadOnly(False)
        self.comboBox_pip_list.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.comboBox_pip_list.currentTextChanged.connect(self.on_comboBox_existing_currentTextChanged)
        self.button_pip_list = PrimaryDropDownPushButton(FluentIcon.ADD_TO, '操作')
        menu = RoundMenu(parent=self.button_pip_list)
        menu.addAction(Action(FluentIcon.UPDATE, '获取/更新', triggered=self.get_pip_list))
        menu.addAction(Action(FluentIcon.PRINT, '安装模块', triggered=self.install_pip_list))
        menu.addAction(Action(FluentIcon.UPDATE, '更新模块', triggered=self.upgrade_pip_list))
        menu.addAction(Action(FluentIcon.ROBOT, '卸载模块', triggered=self.uninstall_pip_list))
        self.button_pip_list.setMenu(menu)
        self.widget_pip_list.addStretch(1)
        self.widget_pip_list.addWidget(self.spinner_pip_list)
        self.widget_pip_list.addWidget(self.comboBox_pip_list)
        self.widget_pip_list.addWidget(self.button_pip_list)
        self.card_pip.addWidget(self.widget_pip_list)

        self.card_editor = SettingGroupCard(FluentIcon.SETTING, "编辑设置", "",
                                           self.scrollAreaWidgetContents)
        self.gridLayout1.addWidget(self.card_editor, 6, 0, 1, 1)

        self.widget_editor = SettingCardWidget('', '编辑器', '可执行文件', self.card_editor)
        self.comboBox_editor_file = EditableComboBox(self.card_editor)
        self.comboBox_editor_file.setClearButtonEnabled(True)
        self.comboBox_editor_file.setMinimumWidth(200)
        self.comboBox_editor_file.addItems(CURRENT_SETTINGS["settings"]["editors"])
        self.comboBox_editor_file.currentTextChanged.connect(self.on_comboBox_editor_file_currentTextChanged)
        self.comboBox_editor_file.returnPressed.connect(self.on_comboBox_editor_file_returnPressed)
        self.comboBox_editor_file.textItemDeleted.connect(self.on_comboBox_editor_file_textItemDeleted)
        self.widget_editor.addWidget(self.comboBox_editor_file)
        self.card_editor.addWidget(self.widget_editor)


        self.card_about = SettingGroupCard(FluentIcon.SETTING, "关于", "",
                                          self.scrollAreaWidgetContents)
        self.gridLayout1.addWidget(self.card_about, 7, 0, 1, 1)

        line_version = LineSettingCardWidget('', "版本", "", self.card_about)
        line_version.setText(VERSION)
        self.card_about.addWidget(line_version)

        line_date = LineSettingCardWidget('', "日期", "", self.card_about)
        line_date.setText(PackageTime)
        self.card_about.addWidget(line_date)

        line_author = LineSettingCardWidget('', "作者", "", self.card_about)
        line_author.setText("Reiner")
        self.card_about.addWidget(line_author)

        line_email = LineSettingCardWidget('', "邮箱", "", self.card_about)
        line_email.setText("nbxlhc@hotmail.com")
        line_email.line.setMinimumWidth(160)
        self.card_about.addWidget(line_email)

        repo = HyperlinkCardWidget('', "仓库", "github", self.card_about)
        repo.setButtonUrl("https://github.com/Reinering/PyQt-Creator.git")
        repo.setButtonText("打开REPO页面")
        self.card_about.addWidget(repo)

        self.verticalSpacer = QSpacerItem(0, 1000, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.gridLayout1.addItem(self.verticalSpacer)

    def configure(self):
        if CURRENT_SETTINGS["settings"]["theme"] == "Dark":
            self.theme.setChecked(True)

        self.theme.switch.checkedChanged.connect(self.on_theme_switch_checkedChanged)

        if CURRENT_SETTINGS["settings"]["mode"] in SETTINGS["settings"]["python_env_modes"]:
            self.comboBox_mode.setCurrentText(CURRENT_SETTINGS["settings"]["mode"])

            if CURRENT_SETTINGS["settings"]["mode"] == "现有环境":
                self.widget_env.show()
                self.widget_teminal.show()
                self.card_pyenv.hide()
                self.card_pyenv_venv.hide()
                self.card_pip.hide()

        if CURRENT_SETTINGS["settings"]["custom_python_path"]:
            self.button_filepath.setText(CURRENT_SETTINGS["settings"]["custom_python_path"])

        if CURRENT_SETTINGS["settings"]["pyenv_path"]:
            self.button_pyenv_path.setText(CURRENT_SETTINGS["settings"]["pyenv_path"])
        else:
            self.button_pyenv_path.setText(LIBS["pyenv"])

        if CURRENT_SETTINGS["settings"]["pyenv_current_version"]:
            self.comboBox_existing.setCurrentText(CURRENT_SETTINGS["settings"]["pyenv_current_version"])

        if CURRENT_SETTINGS["settings"]["pyenv_venv_current_version"]:
            self.comboBox_existing.setCurrentText(CURRENT_SETTINGS["settings"]["pyenv_venv_current_version"])

        if CURRENT_SETTINGS["settings"]["pyenv_mirror_url"]:
            self.widget_pyenv_mirror_url.setCurrentText(CURRENT_SETTINGS["settings"]["pyenv_mirror_url"])

        if CURRENT_SETTINGS["settings"]["pip_mirror_url"]:
            self.widget_pip_mirror_url.setCurrentText(CURRENT_SETTINGS["settings"]["pip_mirror_url"])

        if CURRENT_SETTINGS["settings"]["editor"]:
            self.comboBox_editor_file.setCurrentText(CURRENT_SETTINGS["settings"]["editor"])

        if check_path_in_path(os.path.join("%PYENV_HOME%", 'bin'), "system"):
            self.button_add_PATH.setEnabled(False)

    def getPyPath(self):
        path = ""
        if self.comboBox_mode.currentText() == "现有环境":
            if not self.button_filepath.text():
                Message.error("错误", "请设置Python环境", self)
                return path
            path = self.button_filepath.text()
            return path
        elif self.comboBox_mode.currentText() == "Pyenv 环境":
            if not self.comboBox_existing.currentText():
                Message.error("错误", "请设置Pyenv环境", self)
                return path
            path = os.path.join(CURRENT_SETTINGS["settings"]["pyenv_path"], "versions", self.comboBox_existing.currentText(), "python.exe")
        elif self.comboBox_mode.currentText() == "Pyenv-venv 环境":
            if not self.comboBox_existing.currentText():
                Message.error("错误", "请设置Pyenv-venv 环境", self)
                return path
            path = os.path.join(CURRENT_SETTINGS["settings"]["pyenv_path"], "envs", self.comboBox_venv_existing.currentText(), "Scripts", "python.exe")
        return path

    def new_install(self):
        version = self.comboBox_new_ver.currentText()
        if not version:
            return

        if self.comboBox_new_maxbit.currentText() == "x86":
            version += "-win32"

        if self.venvMangerTh.isRunning():
            Message.error("错误", "pyenv忙碌中，请稍后重试", self)
            return

        self.venvMangerTh.setPyenvPath(CURRENT_SETTINGS["settings"]["pyenv_path"])
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

        self.venvMangerTh.setPyenvPath(CURRENT_SETTINGS["settings"]["pyenv_path"])
        self.venvMangerTh.setCMD("update")
        self.venvMangerTh.start()
        self.button_new_install.setEnabled(False)
        self.spinner_new.setState(True)
        self.spinner_new.show()

    def existing_setGlobal(self):
        if not self.comboBox_existing.currentText():
            return

        if self.venvMangerTh.isRunning():
            Message.error("错误", "pyenv忙碌中，请稍后重试", self)
            return

        self.venvMangerTh.setPyenvPath(CURRENT_SETTINGS["settings"]["pyenv_path"])
        self.venvMangerTh.setCMD("global", self.comboBox_existing.currentText())
        self.venvMangerTh.start()
        self.button_existing_uninstall.setEnabled(False)
        self.spinner_existing.setState(True)
        self.spinner_existing.show()
        Message.info("设置", "设置中，请稍后", self)

    def existing_uninstall(self):
        if self.comboBox_existing.currentText():
            if self.venvMangerTh.isRunning():
                Message.error("错误", "pyenv忙碌中，请稍后重试", self)
                return

            self.venvMangerTh.setPyenvPath(CURRENT_SETTINGS["settings"]["pyenv_path"])
            self.venvMangerTh.setCMD("uninstall", self.comboBox_existing.currentText())
            self.venvMangerTh.start()
            self.button_existing_uninstall.setEnabled(False)
            self.spinner_existing.show()
            self.spinner_existing.setState(True)
            Message.info("卸载", "卸载中，请稍后", self)

    def existing_update(self):
        print("existing_update")
        if os.path.exists(os.path.join(CURRENT_SETTINGS["settings"]["pyenv_path"], "versions")):
            if self.venvMangerTh.isRunning():
                Message.error("错误", "pyenv忙碌中，请稍后重试", self)
                return

            self.venvMangerTh.setPyenvPath(CURRENT_SETTINGS["settings"]["pyenv_path"])
            self.venvMangerTh.setCMD("versions")
            self.venvMangerTh.start()
            self.button_existing_uninstall.setEnabled(False)
            self.spinner_existing.setState(True)
            self.spinner_existing.show()
        else:
            os.mkdir(os.path.join(CURRENT_SETTINGS["settings"]["pyenv_path"], "versions"))
            # Message.error("错误", "Pyenv路径错误", self)

    def get_pip_list(self):
        if self.venvMangerTh.isRunning():
            Message.error("错误", "pyenv忙碌中，请稍后重试", self)
            return

        path = self.getPyPath()
        if not path:
            Message.error("错误", "python解释器获取失败", self)
            return
        if not Path(path).is_absolute():
            path = str(Path(path).absolute())

        self.venvMangerTh.setPyInterpreter(path)
        self.venvMangerTh.setCMD("pip_list", "list")
        self.venvMangerTh.start()

        self.button_pip_list.setEnabled(False)
        self.spinner_pip_list.setState(True)
        self.spinner_pip_list.show()

    def install_pip_list(self):
        if self.venvMangerTh.isRunning():
            Message.error("错误", "pyenv忙碌中，请稍后重试", self)
            return

        if not self.comboBox_pip_list.currentText():
            Message.error("错误", "模块名不能为空", self)
            return

        path = self.getPyPath()
        if not path:
            Message.error("错误", "python解释器获取失败", self)
            return
        if not Path(path).is_absolute():
            path = str(Path(path).absolute())

        self.venvMangerTh.setPyInterpreter(path)
        self.venvMangerTh.setCMD("pip_install", self.comboBox_pip_list.currentText())
        self.venvMangerTh.start()

        self.button_pip_list.setEnabled(False)
        self.spinner_pip_list.setState(True)
        self.spinner_pip_list.show()

    def upgrade_pip_list(self):
        if self.venvMangerTh.isRunning():
            Message.error("错误", "pyenv忙碌中，请稍后重试", self)
            return

        path = self.getPyPath()
        if not path:
            Message.error("错误", "python解释器获取失败", self)
            return
        if not Path(path).is_absolute():
            path = str(Path(path).absolute())

        tmpp = self.comboBox_pip_list.selectedTexts()
        if not tmpp:
            Message.error("错误", "请选择更新的模块", self)
            return

        tmp = []
        for p in tmpp:
            if not p:
                continue
            tmp.append(p.split('-')[0])

        self.venvMangerTh.setPyInterpreter(path)
        self.venvMangerTh.setCMD("pip_upgrade", tmp)
        self.venvMangerTh.start()

        self.button_pip_list.setEnabled(False)
        self.spinner_pip_list.setState(True)
        self.spinner_pip_list.show()

    def uninstall_pip_list(self):
        if self.venvMangerTh.isRunning():
            Message.error("错误", "pyenv忙碌中，请稍后重试", self)
            return

        path = self.getPyPath()
        if not path:
            Message.error("错误", "python解释器获取失败", self)
            return
        if not Path(path).is_absolute():
            path = str(Path(path).absolute())

        tmpp = self.comboBox_pip_list.selectedTexts()
        if not tmpp:
            Message.error("错误", "请选择卸载的模块", self)
            return
        tmp = []
        for p in tmpp:
            if not p:
                continue
            tmp.append(p.split('-')[0])

        self.venvMangerTh.setPyInterpreter(path)
        self.venvMangerTh.setCMD("pip_uninstall", tmp)
        self.venvMangerTh.start()

        self.button_pip_list.setEnabled(False)
        self.spinner_pip_list.setState(True)
        self.spinner_pip_list.show()

    def on_comboBox_mode_currentTextChanged(self, text):
        CURRENT_SETTINGS["settings"]["mode"] = text
        if text == "现有环境":
            self.widget_env.show()
            self.card_pyenv.hide()
            self.card_pyenv_venv.hide()
        elif text == "Pyenv 环境":
            self.widget_env.hide()
            self.card_pyenv.show()
            self.card_pyenv_venv.show()
        elif text == "Pyenv-venv 环境":
            self.widget_env.hide()
            self.card_pyenv.show()
            self.card_pyenv_venv.show()
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

    def on_button_teminal_clicked(self):
        path = self.getPyPath()
        if not path:
            Message.error("错误", "python解释器获取失败", self)
            return
        if not Path(path).is_absolute():
            path = str(Path(path).absolute())
        print("open cmd:", path)
        startCMD(path)

    def on_button_pyenv_path_textChanged(self, text):
        if self.initState:
            return

        print("mark:", text, os.path.exists(text))
        if text and os.path.exists(text):
            print("mark")
            CURRENT_SETTINGS["settings"]["pyenv_path"] = text.replace("/", "\\")
            write_config()

            if self.venvMangerTh.isRunning():
                Message.error("错误", "pyenv忙碌中，请稍后重试", self)
                return

            print("set pyenv path:", CURRENT_SETTINGS["settings"]["pyenv_path"])
            self.venvMangerTh.setPyenvPath(CURRENT_SETTINGS["settings"]["pyenv_path"])
            self.venvMangerTh.setPyenvVenvPath(CURRENT_SETTINGS["settings"]["pyenv_path"])
            print("set pyenv path:", self.venvMangerTh.pyenvManger.venvPath)
            self.venvMangerTh.setCMD("init")
            self.venvMangerTh.start()

    def on_button_pyenv_path_returnPressed(self):
        if self.initState:
            return

        text = self.button_pyenv_path.text()
        if text and os.path.exists(text):
            CURRENT_SETTINGS["settings"]["pyenv_path"] = text.replace("/", "\\")
            write_config()

            if self.venvMangerTh.isRunning():
                Message.error("错误", "pyenv忙碌中，请稍后重试", self)
                return

            self.venvMangerTh.setPyenvPath(CURRENT_SETTINGS["settings"]["pyenv_path"])
            self.venvMangerTh.setPyenvVenvPath(CURRENT_SETTINGS["settings"]["pyenv_path"])
            self.venvMangerTh.setCMD("init")
            self.venvMangerTh.start()

    def on_button_pyenv_path_refresh_clicked(self):
        if self.venvMangerTh.isRunning():
            Message.error("错误", "pyenv忙碌中，请稍后重试", self)
            return

        self.venvMangerTh.setCMD("init")
        self.venvMangerTh.start()

    def on_button_add_PATH_clicked(self):
        if not is_admin():
            Message.error("错误", "请以管理员权限运行", self)
            return

        if os.path.isabs(CURRENT_SETTINGS["settings"]["pyenv_path"]):
            path = CURRENT_SETTINGS["settings"]["pyenv_path"]
        else:
            path = os.path.join(BUNDLE_DIR, CURRENT_SETTINGS["settings"]["pyenv_path"])


        set_environment_variable("PYENV_HOME", path, "system")
        append_to_path(os.path.join("%PYENV_HOME%", "bin"), "system")
        append_to_path(os.path.join("%PYENV_HOME%", "shims"), "system")

        Message.info("成功", "环境变量添加成功", self)

        self.button_add_PATH.setEnabled(False)

    def on_comboBox_existing_currentTextChanged(self, text):
        if not self.initState:
            CURRENT_SETTINGS["settings"]["pyenv_current_version"] = text.replace("/", "\\")
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

    def venv_existing_refresh(self):
        print("venv_existing_refresh")

        if os.path.exists(os.path.join(CURRENT_SETTINGS["settings"]["pyenv_path"], "envs")):
            if self.venvMangerTh.isRunning():
                Message.error("错误", "pyenv忙碌中，请稍后重试", self)
                return
            self.venvMangerTh.setPyenvVenvPath(CURRENT_SETTINGS["settings"]["pyenv_path"])
            self.venvMangerTh.setCMD("list_envs")
            self.venvMangerTh.start()
            self.button_venv_existing_uninstall.setEnabled(False)
            self.spinner_venv_existing.setState(True)
            self.spinner_venv_existing.show()
        else:
            os.mkdir(os.path.join(CURRENT_SETTINGS["settings"]["pyenv_path"], "envs"))
            # Message.error("错误", "Pyenv路径错误", self)

    def venv_existing_uninstall(self):
        if self.comboBox_venv_existing.currentText():
            if self.venvMangerTh.isRunning():
                Message.error("错误", "pyenv忙碌中，请稍后重试", self)
                return

            self.venvMangerTh.setPyenvPath(CURRENT_SETTINGS["settings"]["pyenv_path"])
            self.venvMangerTh.setCMD("uninstall_env", self.comboBox_venv_existing.currentText())
            self.venvMangerTh.start()
            self.button_venv_existing_uninstall.setEnabled(False)
            self.spinner_venv_existing.show()
            self.spinner_venv_existing.setState(True)
            Message.info("卸载", "卸载中，请稍后", self)

    def on_button_venv_install_clicked(self):
        if not self.comboBox_existing.currentText():
            Message.error("错误", "请选择pyenv环境", self)
            return

        if not self.lineEdit_venv_install.text():
            Message.error("错误", "请输入pyenv-venv环境名称", self)
            return

        if self.venvMangerTh.isRunning():
            Message.error("错误", "pyenv忙碌中，请稍后重试", self)
            return

        self.venvMangerTh.setPyenvPath(CURRENT_SETTINGS["settings"]["pyenv_path"])
        self.venvMangerTh.setCMD("install_env", self.comboBox_existing.currentText(), self.lineEdit_venv_install.text())
        self.venvMangerTh.start()
        self.button_venv_install.setEnabled(False)
        self.spinner_venv_install.show()
        self.spinner_venv_install.setState(True)
        Message.info("创建", "创建中，请稍后", self)

    def on_comboBox_venv_existing_currentTextChanged(self, text):
        if not self.initState:
            CURRENT_SETTINGS["settings"]["pyenv_venv_current_version"] = text.replace("/", "\\")
            write_config()

    def on_button_venv_teminal_clicked(self):
        if not self.comboBox_venv_existing.currentText():
            Message.error("错误", "请设置pyenv-venv环境", self)
            return

        path = os.path.join(CURRENT_SETTINGS["settings"]["pyenv_path"], "bin", "pyenv-venv.bat")
        if not Path(path).is_absolute():
            path = str(Path(path).absolute())

        os.system(f' start cmd.exe /K {path} activate {self.comboBox_venv_existing.currentText()}')

    def on_comboBox_pip_mirror_url_currentTextChanged(self, text):
        CURRENT_SETTINGS["settings"]["pip_mirror_url"] = text

        write_config()

    def on_button_existing_uninstall_clicked(self):
        if self.comboBox_existing.currentText():
            if self.venvMangerTh.isRunning():
                Message.error("错误", "pyenv忙碌中，请稍后重试", self)
                return

            self.venvMangerTh.setPyenvPath(CURRENT_SETTINGS["settings"]["pyenv_path"])
            self.venvMangerTh.setCMD("uninstall", self.comboBox_existing.currentText())
            self.venvMangerTh.start()
            self.button_existing_uninstall.setEnabled(False)
            self.spinner_existing.show()
            self.spinner_existing.setState(True)

            Message.info("卸载", "卸载中，请稍后", self)

    def on_comboBox_editor_file_currentTextChanged(self, text):
        if text:
            CURRENT_SETTINGS["settings"]["editor"] = text
            write_config()

    def on_comboBox_editor_file_returnPressed(self):
        text = self.comboBox_editor_file.text()
        if text:
            CURRENT_SETTINGS["settings"]["editors"].append(text)
            write_config()

    def on_comboBox_editor_file_textItemDeleted(self, text):
        if text:
            try:
                CURRENT_SETTINGS["settings"]["editors"].remove(text)
            except Exception as e:
                logging.error(e)

            write_config()

    def on_theme_switch_checkedChanged(self, state):
        if state:
            toggleTheme()
            CURRENT_SETTINGS["settings"]["theme"] = "Dark"
        else:
            toggleTheme()
            CURRENT_SETTINGS["settings"]["theme"] = "Light"

        write_config()

    def receive_VMresult(self, cmd, result, isClose=True):
        print(f"receive_VMresult: {cmd}, {result}")
        logging.debug(f"receive_VMresult: {cmd}, {result}")
        if isinstance(result[1], list) and len(result[1]) > 5:
            output = result[1][-5:]
        else:
            output = result[1]

        if cmd == "init":
            self.initState = False
            try:
                self.configure()
            except Exception as e:
                logging.error(e)
                QMessageBox.critical(self, "初始化错误", f"请检查配置文件{str(e)}")
                raise Exception(f"请检查配置文件{str(e)}")
        elif cmd == "py_version":
            if not result[0]:
                Message.error("解释器错误", output, self)
                return
            self.label_ver.setText("版本: " + result[1].strip('\n'))
            CURRENT_SETTINGS["settings"]["custom_python_path"] = self.button_filepath.text()
            write_config()
        elif cmd == "list":
            if not result[0]:
                Message.error("错误", output, self)
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
                Message.error("错误", output, self)
                return

            self.venvMangerTh.stop()
            self.venvMangerTh.setPyenvPath(CURRENT_SETTINGS["settings"]["pyenv_path"])
            self.venvMangerTh.setCMD("list")
            self.venvMangerTh.start()
            return
        elif cmd == "install":
            self.button_new_install.setEnabled(True)
            self.spinner_new.setState(False)
            self.spinner_new.hide()

            if not result[0]:
                Message.error("错误", output, self)
                return

            Message.info("成功", "安装成功", self)

            self.venvMangerTh.stop()
            self.existing_update()
            return
        elif cmd == "uninstall":
            self.button_existing_uninstall.setEnabled(True)
            self.spinner_existing.setState(False)
            self.spinner_existing.hide()

            if not result[0]:
                Message.error("错误", output, self)
                return

            Message.info("成功", "卸载成功", self)

            self.venvMangerTh.stop()
            self.existing_update()
            return
        elif cmd == "versions":
            self.button_existing_uninstall.setEnabled(True)
            self.spinner_existing.setState(False)
            self.spinner_existing.hide()

            if not result[0]:
                Message.error("错误", output, self)
                return

            result = list(filter(None, result[1].split("\n")))
            tmp = []
            for res in result:
                res.strip()
                if '*' == res[0]:
                    tmp.append(res.split(' (')[0][1:].strip())
                    self.lineEdit_global_ver.setText(res.split(' (')[0][1:])
                else:
                    tmp.append(res.strip())
            if tmp:
                self.comboBox_existing.clear()
                self.comboBox_existing.addItems(tmp)
        elif cmd == "global":
            self.button_existing_uninstall.setEnabled(True)
            self.spinner_existing.setState(False)
            self.spinner_existing.hide()

            if not result[0]:
                Message.error("错误", output, self)
                return

            self.lineEdit_global_ver.setText(self.comboBox_existing.currentText())

            Message.info("成功", "设置Global成功", self)
        elif cmd == "list_envs":
            self.button_venv_existing_uninstall.setEnabled(True)
            self.spinner_venv_existing.setState(False)
            self.spinner_venv_existing.hide()

            if not result[0]:
                Message.error("错误", output, self)
                return

            if not result[1]:
                Message.error("错误", "查询错误", self)
                return

            result = list(filter(None, result[1].split("\n")[1:]))
            tmp = []
            for res in result:
                res.strip()
                tmp.append(res.strip())

            self.comboBox_venv_existing.clear()
            if tmp:
                self.comboBox_venv_existing.addItems(tmp)

            if CURRENT_SETTINGS["settings"]["pyenv_venv_current_version"] in tmp:
                self.comboBox_venv_existing.setCurrentText(CURRENT_SETTINGS["settings"]["pyenv_venv_current_version"])
        elif cmd == "uninstall_env":
            self.button_venv_existing_uninstall.setEnabled(True)
            self.spinner_venv_existing.setState(False)
            self.spinner_venv_existing.hide()

            if not result[0]:
                Message.error("错误", output, self)
                return

            Message.info("成功", "卸载成功", self)

            self.venvMangerTh.stop()
            self.venv_existing_refresh()
            return
        elif cmd == "install_env":
            self.button_venv_install.setEnabled(True)
            self.spinner_venv_install.setState(False)
            self.spinner_venv_install.hide()

            if not result[0]:
                Message.error("错误", output, self)
                return

            if "already exists. Please choose another name for the env" in output:
                Message.error("错误", "环境已存在", self)
            else:
                self.lineEdit_venv_install.clear()
                Message.info("成功", "创建成功", self)

                self.venvMangerTh.stop()
                self.venv_existing_refresh()
                return

        elif cmd == "pip_list":
            self.button_pip_list.setEnabled(True)
            self.spinner_pip_list.setState(False)
            self.spinner_pip_list.hide()
            if not result[0]:
                Message.error("错误", output, self)
                return

            result = list(filter(None, result[1].split("\n")))
            tmp = []
            maxLen = 0
            for res in result:
                if "Package" in res:
                    continue
                elif "------" in res:
                    continue

                tmpp = res.split(' ')
                tmpp = f"{tmpp[0].strip(' ')}-{tmpp[-1].strip(' ')}"
                if len(tmpp) > maxLen:
                    maxLen = len(tmpp)
                tmp.append(tmpp)
            if tmp:
                self.comboBox_pip_list.clear()
                self.comboBox_pip_list.addItems(tmp)
                self.comboBox_pip_list.setMinimumWidth(maxLen*9*0.93)
        elif cmd == "pip_install":
            self.button_pip_list.setEnabled(True)
            self.spinner_pip_list.setState(False)
            self.spinner_pip_list.hide()
            if not result[0]:
                Message.error("错误", output, self)
                return

            Message.info("成功", "安装成功", self)
        elif cmd == "pip_upgrade":
            self.button_pip_list.setEnabled(True)
            self.spinner_pip_list.setState(False)
            self.spinner_pip_list.hide()
            if not result[0]:
                Message.error("错误", output, self)
                return

            self.comboBox_pip_list.clearSelected()
            Message.info("成功", "更新成功", self)
        elif cmd == "pip_uninstall":
            self.button_pip_list.setEnabled(True)
            self.spinner_pip_list.setState(False)
            self.spinner_pip_list.hide()
            if not result[0]:
                Message.error("错误", output, self)
                return

            self.comboBox_pip_list.clearSelected()
            Message.info("成功", "卸载成功", self)
        else:
            pass

        if isClose:
            self.venvMangerTh.stop()


class VenvManagerThread(QThread):

    signal_result = Signal(str, tuple, bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.pyenvManger = PyenvManager(LIBS["pyenv"])
        self.pyenvVenvManger = PyenvVenvManager(LIBS["pyenv"])
        self.pyI = PyInterpreter()
        self.stopBool = False

    def stop(self):
        try:
            self.stopBool = True
            self.pyI.stop()
            self.terminate()
            self.stopBool = False  # 增加：确保下次可正常启动
        except Exception as e:
            print(e)

    def setCMD(self, cmd, *args, **kwargs):
        self.cmd = cmd
        self.args = args
        self.kwargs = kwargs

    def setPyenvPath(self, path):
        self.pyenvManger.setVenvPath(path)

    def setPyenvVenvPath(self, path):
        self.pyenvVenvManger.setVenvPath(path)

    def setPyInterpreter(self, path):
        self.pyI.setInterpreter(path)

    def run(self):
        self.stopBool = False  # 增加：每次启动线程时重置
        cmd = self.cmd
        if cmd == "py_version":
            result = self.pyI.version()
            self.signal_result.emit(cmd, result)
        elif cmd == "init":
            result = self.pyenvManger.list()
            self.signal_result.emit("list", result, False)
            result = self.pyenvManger.versions()
            self.signal_result.emit("versions", result, False)
            result = self.pyenvVenvManger.envs()
            self.signal_result.emit("list_envs", result, False)

            self.signal_result.emit("init", result, True)
        elif cmd == "list":
            result = self.pyenvManger.list()
            self.signal_result.emit(cmd, result, True)
        elif cmd == "update":
            result = self.pyenvManger.update()
            self.signal_result.emit(cmd, result, True)
        elif cmd == "install":
            result = self.pyenvManger.install(self.args[0])
            self.signal_result.emit(cmd, result, True)
            self.pyenvManger.rehash()
        elif cmd == "uninstall":
            result = self.pyenvManger.uninstall(self.args[0])
            self.signal_result.emit(cmd, result, True)
        elif cmd == "environ":
            self.pyenvManger.setEnviron(**self.kwargs)
        elif cmd == "versions":
            result = self.pyenvManger.versions()
            self.signal_result.emit(cmd, result, True)
        elif cmd == "global":
            result = self.pyenvManger.global_(self.args[0])
            self.signal_result.emit(cmd, result, True)
        elif cmd == "list_envs":
            result = self.pyenvVenvManger.envs()
            self.signal_result.emit(cmd, result, True)
        elif cmd == "uninstall_env":
            result = self.pyenvVenvManger.uninstall(self.args[0])
            self.signal_result.emit(cmd, result, True)
        elif cmd == "install_env":
            result = self.pyenvVenvManger.install(self.args[0], self.args[1])
            self.signal_result.emit(cmd, result, True)
        elif cmd == "pip_list":
            result = self.pyI.pip(self.args[0])
            self.signal_result.emit(cmd, result, True)
        elif cmd == "pip_install":
            result = self.pyI.pip("install", self.args[0])
            self.signal_result.emit(cmd, result, True)
        elif cmd == "pip_upgrade":
            tmp = ["install", "--upgrade"]
            tmp.extend(self.args[0])
            result = self.pyI.pip(*tmp)
            self.signal_result.emit(cmd, result, True)
        elif cmd == "pip_uninstall":
            tmp = ["uninstall", "-y"]
            tmp.extend(self.args[0])
            result = self.pyI.pip(*tmp)
            self.signal_result.emit(cmd, result, True)
        else:
            self.signal_result.emit(cmd, ["False", "未知命令"], True)

