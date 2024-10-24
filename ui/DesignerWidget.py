#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author: Reiner New
email: nbxlc@hotmail.com
Module implementing DesignerWidget.
"""


from PySide6.QtCore import Slot, Qt, QRect, QThread, Signal
from PySide6.QtWidgets import QWidget, QGridLayout, QHBoxLayout, QVBoxLayout, QSpacerItem, QSizePolicy, QMessageBox
import os
import logging
from pathlib import Path

from qfluentwidgets import (
    ScrollArea,
    PrimaryPushButton,
    ComboBox,
    BodyLabel, TitleLabel, CaptionLabel,
    CardWidget,
    IconWidget,
    SettingCard,
    PrimaryDropDownPushButton,
    RoundMenu,
    Action
)
from qfluentwidgets.common.icon import FluentIcon
from qfluentwidgets.components.settings.setting_card import SettingIconWidget

from qfluentexpand.components.card.settingcard import SettingGroupCard, ComboBoxSettingCard
from qfluentexpand.components.line.selector import FilePathSelector
from qfluentexpand.components.label.label import GifLabel
from qfluentexpand.common.gif import APPGIF
from qfluentexpand.components.widgets.card import SettingCardWidget, ComboBoxSettingCardWidget, FileSettingCardWidget

from .Ui_DesignerWidget import Ui_Form
from .utils.stylesheets import StyleSheet
from .utils.config import write_config
from .utils.tool import startCMD
from .compoments.info import Message
from common.pyenv import PyVenvManager
from common.py import PyInterpreter, PyPath
from qfluentexpand.tools import designer
from manage import LIBS, SETTINGS, CURRENT_SETTINGS, REQUIREMENTS_URLS


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

        self.button_open = PrimaryDropDownPushButton(FluentIcon.BRUSH, '打开')
        menu = RoundMenu(parent=self.button_open)
        menu.addAction(Action(FluentIcon.CONNECT, '原生', triggered=self.open_origin))
        menu.addAction(Action(FluentIcon.ALBUM, '插件', triggered=self.open_plugin))
        self.button_open.setMenu(menu)

        hBoxLayout.addWidget(self.button_open, 0, Qt.AlignmentFlag.AlignRight)

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

        self.file_ui = FileSettingCardWidget('', "UI 文件", "", self.envCard)
        self.file_ui.setFileTypes("UI 文件 (*.ui)")
        self.file_ui.selector.setReadOnly(False)
        self.file_ui.selector.setMinimumWidth(200)
        self.file_ui.textChanged.connect(self.on_button_file_ui_textChanged)
        self.envCard.addWidget(self.file_ui)

        self.designerSetCard = SettingGroupCard(FluentIcon.SETTING, "Desinger 设置", "",
                                                self.scrollAreaWidgetContents)
        self.gridLayout1.addWidget(self.designerSetCard, 2, 0, 1, 1)
        widget = QWidget(self.designerSetCard)
        label_designer_install = BodyLabel("安装Designer环境")
        self.spinner_designer_install = GifLabel(self.designerSetCard)
        self.spinner_designer_install.setGif(APPGIF.LOADING)
        self.spinner_designer_install.setFixedSize(30, 30)
        self.spinner_designer_install.hide()
        self.button_designer_install = PrimaryPushButton(self.designerSetCard)
        self.button_designer_install.setText("安装")
        self.button_designer_install.clicked.connect(self.on_button_designer_install_clicked)
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(30, 5, 30, 5)
        layout.addWidget(label_designer_install)
        layout.addStretch(1)
        layout.addWidget(self.spinner_designer_install)
        layout.addWidget(self.button_designer_install)
        self.designerSetCard.addWidget(widget)

        widget_plugin = QWidget(self.designerSetCard)
        label_designer_plugin_install = BodyLabel("安装第三方插件")
        self.spinner_designer_plugin_install = GifLabel(self.designerSetCard)
        self.spinner_designer_plugin_install.setGif(APPGIF.LOADING)
        self.spinner_designer_plugin_install.setFixedSize(30, 30)
        self.spinner_designer_plugin_install.hide()
        self.button_designer_thirdplugin = PrimaryDropDownPushButton(FluentIcon.MAIL, '操作')
        menu = RoundMenu(parent=self.button_designer_thirdplugin)
        menu.addAction(Action(FluentIcon.PRINT, '安装', triggered=self.thirdplugin_install))
        menu.addAction(Action(FluentIcon.UPDATE, '更新', triggered=self.thirdplugin_upgrade))
        menu.addAction(Action(FluentIcon.ROBOT, '卸载', triggered=self.thirdplugin_uninstall))
        self.button_designer_thirdplugin.setMenu(menu)

        layout = QHBoxLayout(widget_plugin)
        layout.setContentsMargins(30, 5, 30, 5)
        layout.addWidget(label_designer_plugin_install)
        layout.addStretch(1)
        layout.addWidget(self.spinner_designer_plugin_install)
        layout.addWidget(self.button_designer_thirdplugin)
        self.designerSetCard.addWidget(widget_plugin)


        self.verticalSpacer = QSpacerItem(0, 1000, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.gridLayout1.addItem(self.verticalSpacer, 3, 0, 1, 1)

        try:
            self.configure()
        except Exception as e:
            logging.error(e)
            QMessageBox.critical(self, "初始化错误", f"请检查配置文件{str(e)}")
            raise Exception(f"请检查配置文件{str(e)}")

    def configure(self):
        if CURRENT_SETTINGS["designer"]["mode"] in SETTINGS["designer"]["python_env_modes"]:
            self.comboBox_mode.setCurrentText(CURRENT_SETTINGS["designer"]["mode"])

        if CURRENT_SETTINGS["designer"]["custom_python_path"]:
            self.button_filepath.setText(CURRENT_SETTINGS["designer"]["custom_python_path"])

        if CURRENT_SETTINGS["designer"]["fileUI"]:
            self.file_ui.setText(CURRENT_SETTINGS["designer"]["fileUI"])

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

    def open_origin(self):
        if self.venvMangerTh.isRunning():
            Message.error("错误", "env忙碌中，请稍后重试", self)
            return

        path = self.getPyPath()
        if not path:
            Message.error("错误", "python解释器获取失败", self)
            return

        self.venvMangerTh.setPyInterpreter(path)

        if self.file_ui.text():
            self.venvMangerTh.setCMD("designer", PyPath.PYSIDE6_DESIGNER.path(path), self.file_ui.text())
        else:
            self.venvMangerTh.setCMD("designer", PyPath.PYSIDE6_DESIGNER.path(path), )
        self.venvMangerTh.start()

        self.button_open.setEnabled(False)

    def open_plugin(self):
        if self.venvMangerTh.isRunning():
            Message.error("错误", "env忙碌中，请稍后重试", self)
            return

        path = self.getPyPath()
        if not path:
            Message.error("错误", "python解释器获取失败", self)
            return

        self.venvMangerTh.setPyInterpreter(path)
        if self.file_ui.text():
            self.venvMangerTh.setCMD("designer_plugin", PyPath.DESIGNER_PYSIDE6.path(path), self.file_ui.text())
        else:
            self.venvMangerTh.setCMD("designer_plugin", PyPath.DESIGNER_PYSIDE6.path(path), )
        self.venvMangerTh.start()

        self.button_open.setEnabled(False)

        Message.info("提示", "启动带插件的designer，有时会卡住，请耐心等候。正常开启后若要关闭请稍等20s...", self)

    def thirdplugin_install(self):
        if self.thirdplugin("thirdplugin_install", REQUIREMENTS_URLS["qfluentwidgets"]["pyside6"]):
            Message.info("提示", "安装中，请稍后", self)

    def thirdplugin_upgrade(self):
        if self.thirdplugin("thirdplugin_upgrade", REQUIREMENTS_URLS["qfluentwidgets"]["pyside6"]):
            Message.info("提示", "更新中，请稍后", self)

    def thirdplugin_uninstall(self):
        if self.thirdplugin("thirdplugin_uninstall", REQUIREMENTS_URLS["qfluentwidgets"]["pyside6"]):
            Message.info("提示", "卸载中，请稍后", self)

    def thirdplugin(self, cmd, args):
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

        self.button_designer_thirdplugin.setEnabled(False)
        self.spinner_designer_plugin_install.setState(True)
        self.spinner_designer_plugin_install.show()

        return True

    def setUIFile(self, file):
        self.comboBox_mode.setCurrentText(SETTINGS["pack"]["python_env_modes"][1])
        self.file_ui.setText(file)

    def on_comboBox_mode_currentTextChanged(self, text):
        CURRENT_SETTINGS["designer"]["mode"] = text

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
        if text and "python.exe" in text:
            self.venvMangerTh.setPyInterpreter(text)
            self.venvMangerTh.setCMD("py_version")
            self.venvMangerTh.start()
        else:
            self.label_ver.setText("版本: ")
            CURRENT_SETTINGS["designer"]["custom_python_path"] = ""
            write_config()

    def on_button_teminal_clicked(self):
        path = self.getPyPath()
        if not path:
            Message.error("错误", "python解释器获取失败", self)
            return
        if not Path(path).is_absolute():
            path = str(Path(path).absolute())

        startCMD(path)

    def on_button_file_ui_textChanged(self, text):
        if text and ".ui" in text:
            CURRENT_SETTINGS["designer"]["fileUI"] = text
            write_config()

    def on_button_designer_install_clicked(self):
        if self.venvMangerTh.isRunning():
            Message.error("错误", "env忙碌中，请稍后重试", self)
            return

        path = self.getPyPath()
        if not path:
            Message.error("错误", "python解释器获取失败", self)
            return

        self.venvMangerTh.setPyInterpreter(path)
        self.venvMangerTh.setCMD("install", "pyside6")
        self.venvMangerTh.start()

        self.button_designer_install.setEnabled(False)
        self.spinner_designer_install.setState(True)
        self.spinner_designer_install.show()
        Message.info("安装", "安装中，请稍后", self)

    def receive_VMresult(self, cmd, result):
        logging.debug(f"receive_VMresult: {cmd}, {result}")
        if isinstance(result[1], list) and len(result[1]) > 5:
            output = result[1][-5:]
        else:
            output = result[1]

        if cmd == "init":
            pass
        elif "py_version" in cmd:
            if not result[0]:
                Message.error("解释器错误", output, self)
                return
            self.label_ver.setText("版本: " + result[1].strip('\n'))
            CURRENT_SETTINGS["designer"]["custom_python_path"] = self.button_filepath.text()
            write_config()
        elif cmd == "install":
            self.button_designer_install.setEnabled(True)
            self.spinner_designer_install.setState(False)
            self.spinner_designer_install.hide()

            if not result[0]:
                Message.error("错误", output, self)
                return

            Message.info("成功", "安装成功", self)
        elif cmd == "designer":
            self.button_open.setEnabled(True)
            if not result[0]:
                Message.error("错误", output, self)
                return
        elif "designer_plugin" in cmd:
            self.button_open.setEnabled(True)
            if not result[0]:
                Message.error("错误", output, self)
                return
        elif "thirdplugin" in cmd:
            self.button_designer_thirdplugin.setEnabled(True)
            self.spinner_designer_plugin_install.setState(False)
            self.spinner_designer_plugin_install.hide()

            if not result[0]:
                Message.error("错误", output, self)
                return

            if "uninstall" in cmd:
                Message.info("成功", "卸载成功", self)
            elif "install" in cmd:
                Message.info("成功", "安装成功", self)
            elif "upgrade" in cmd:
                Message.info("成功", "更新成功", self)
            else:
                Message.error("错误", "命令识别错误", self)
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
        self.stop = True

    def setCMD(self, cmd, *args, **kwargs):
        self.cmd = cmd
        self.args = args
        self.kwargs = kwargs

    def setPyInterpreter(self, path):
        self.pyI.setInterpreter(path)

    def run(self):
        cmd = self.cmd
        if cmd == "init":
            pass
        elif cmd == "environ":
            self.pyI.setEnviron(**self.kwargs)
        elif cmd == "py_version":
            result = self.pyI.version()
            self.signal_result.emit(cmd, result)
        elif cmd == "install":
            result = self.pyI.pip(cmd, *self.args)
            self.signal_result.emit(cmd, result)
        elif cmd == "thirdplugin_install":
            result = self.pyI.pip("install", REQUIREMENTS_URLS["qfluentwidgets"]["pyside6"])
            if not result[0]:
                self.signal_result.emit(cmd, result)
                return
            result = self.pyI.pip("install", "git+" + REQUIREMENTS_URLS["qfluentexpand"] + "@pyside6")
            self.signal_result.emit(cmd, result)
        elif cmd == "thirdplugin_upgrade":
            result = self.pyI.pip("install", "--upgrade", REQUIREMENTS_URLS["qfluentwidgets"]["pyside6"])
            if not result[0]:
                self.signal_result.emit(cmd, result)
                return
            result = self.pyI.pip("install", "--upgrade", "git+" + REQUIREMENTS_URLS["qfluentexpand"] + "@pyside6")
            self.signal_result.emit(cmd, result)
        elif cmd == "thirdplugin_uninstall":
            result = self.pyI.pip("uninstall", "-y", REQUIREMENTS_URLS["qfluentwidgets"]["pyside6"])
            if not result[0]:
                self.signal_result.emit(cmd, result)
                return
            result = self.pyI.pip("uninstall", "-y", "qfluentexpand")
            self.signal_result.emit(cmd, result)
        elif cmd == "designer":
            result = self.pyI.cmd(self.args)
            self.signal_result.emit(cmd, result)
        elif cmd == "designer_plugin":
            result = self.pyI.py_popen(self.args)
            self.signal_result.emit(cmd, result)
        elif cmd == "designer_plugin1":
            result = designer.main()
            self.signal_result.emit(cmd, result)
        else:
            self.signal_result.emit(cmd, ["False", "未知命令"])