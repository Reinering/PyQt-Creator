# -*- coding: utf-8 -*-

"""
Module implementing OtherWidget.
"""

from PySide6.QtCore import Slot, QRect, Qt, QThread, Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget, QGridLayout, QHBoxLayout, QVBoxLayout, QSpacerItem, QSizePolicy, QMessageBox
import os
import simplejson as json
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
from qfluentexpand.components.label.label import GifLabel
from qfluentexpand.common.gif import APPGIF

from .Ui_OtherWidget import Ui_Form
from .GenerateCodeDialog import GenerateCodeDialog
from .utils.stylesheets import StyleSheet
from .utils.config import write_config
from .utils.icon import AppIcon
from .compoments.info import Message
from common.py import PyInterpreter, PyPath
from common.pyinstaller import PyinstallerPackage
from common.pipreqs import Pipreqs

from manage import ROOT_PATH, UI_CONFIG, SettingPath, LIBS, SETTINGS, CURRENT_SETTINGS, REQUIREMENTS_URLS



class OtherWidget(QWidget, Ui_Form):
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
        self.setObjectName("other")
        StyleSheet.OTHER.apply(self)

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

        titleLabel = TitleLabel("Other", self)
        subtitleLabel = CaptionLabel("其他", self)

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
        self.envCard = SettingGroupCard(FluentIcon.SPEED_OFF, "环境设置", "",
                                        self.scrollAreaWidgetContents)
        self.gridLayout1.addWidget(self.envCard, 1, 0, 1, 1)
        widget_mode = QWidget(self.envCard)
        envLabel = BodyLabel("模式")
        self.comboBox_mode = ComboBox(self.envCard)
        self.comboBox_mode.addItems(SETTINGS["other"]["python_env_modes"])
        self.comboBox_mode.currentTextChanged.connect(self.on_comboBox_mode_currentTextChanged)
        layout = QHBoxLayout(widget_mode)
        layout.setContentsMargins(30, 5, 30, 5)
        layout.addWidget(envLabel)
        layout.addStretch(1)
        layout.addWidget(self.comboBox_mode)
        self.envCard.addWidget(widget_mode)

        self.widget_env = QWidget(self.envCard)
        self.label_env = BodyLabel("Python 环境", self.envCard)
        self.label_ver = CaptionLabel("版本: ", self.envCard)
        self.button_filepath = FilePathSelector(self.envCard)
        self.button_filepath.setText("选择")
        self.button_filepath.setFileTypes("python.exe")
        self.button_filepath.setFixedWidth(200)
        self.button_filepath.textChanged.connect(self.on_button_filepath_textChanged)
        layout = QHBoxLayout(self.widget_env)
        layout.setContentsMargins(30, 5, 30, 5)
        layout.addWidget(self.label_env)
        layout.addStretch(1)
        layout.addWidget(self.label_ver)
        layout.addStretch(1)
        layout.addWidget(self.button_filepath)
        self.envCard.addWidget(self.widget_env)

        self.widget_env_project = QWidget(self.envCard)
        envLabel = BodyLabel("项目目录")
        self.button_env_folder = FolderPathSelector(self.envCard)
        self.button_env_folder.setMaximumWidth(300)
        self.button_env_folder.setFixedWidth(200)
        layout = QHBoxLayout(self.widget_env_project)
        layout.setContentsMargins(30, 5, 30, 5)
        layout.addWidget(envLabel)
        layout.addStretch(1)
        layout.addWidget(self.button_env_folder)
        self.envCard.addWidget(self.widget_env_project)

        self.card_requirements = SettingGroupCard(FluentIcon.SPEED_OFF, "pipreqs 设置", "",
                                        self.scrollAreaWidgetContents)
        self.gridLayout1.addWidget(self.card_requirements, 2, 0, 1, 1)

        widget_pipreqs = QWidget(self.card_requirements)
        envLabel = BodyLabel("pipreqs")
        self.spinner_pipreqs = GifLabel(self.card_requirements)
        self.spinner_pipreqs.setGif(APPGIF.LOADING.path())
        self.spinner_pipreqs.setFixedSize(30, 30)
        self.spinner_pipreqs.hide()
        self.button_pipreqs = PrimaryDropDownPushButton(FluentIcon.MAIL, '操作')
        menu = RoundMenu(parent=self.button_pipreqs)
        menu.addAction(Action(FluentIcon.BASKETBALL, '安装', triggered=self.pipreqs_install))
        menu.addAction(Action(FluentIcon.ALBUM, '更新', triggered=self.pipreqs_upgrade))
        menu.addAction(Action(FluentIcon.ALBUM, '卸载', triggered=self.pipreqs_uninstall))
        self.button_pipreqs.setMenu(menu)

        layout = QHBoxLayout(widget_pipreqs)
        layout.setContentsMargins(30, 5, 30, 5)
        layout.addWidget(envLabel)
        layout.addStretch(1)
        layout.addWidget(self.spinner_pipreqs)
        layout.addWidget(self.button_pipreqs)
        self.card_requirements.addWidget(widget_pipreqs)

        widget_pipreqs_edit = QWidget(self.card_requirements)
        envLabel = BodyLabel("pipreqs 配置文件")
        self.button_pipreqs_edit = PrimaryPushButton(self.card_requirements)
        self.button_pipreqs_edit.setText("编辑")
        self.button_pipreqs_edit.clicked.connect(self.on_button_pipreqs_edit_clicked)
        layout = QHBoxLayout(widget_pipreqs_edit)
        layout.setContentsMargins(30, 5, 30, 5)
        layout.addWidget(envLabel)
        layout.addStretch(1)
        layout.addWidget(self.button_pipreqs_edit)
        self.card_requirements.addWidget(widget_pipreqs_edit)

        widget_requirements = QWidget(self.card_requirements)
        envLabel = BodyLabel("requirements")
        self.spinner_requirements = GifLabel(self.card_requirements)
        self.spinner_requirements.setGif(APPGIF.LOADING.path())
        self.spinner_requirements.setFixedSize(30, 30)
        self.spinner_requirements.hide()

        self.button_requirements = PrimaryDropDownPushButton(FluentIcon.MAIL, '操作')
        menu = RoundMenu(parent=self.button_requirements)
        menu.addAction(Action(FluentIcon.BASKETBALL, '生成', triggered=self.generate_requirements))
        menu.addAction(Action(FluentIcon.ALBUM, '安装', triggered=self.install_requirements))
        menu.addAction(Action(FluentIcon.ALBUM, '编辑', triggered=self.edit_requirements))
        self.button_requirements.setMenu(menu)
        layout = QHBoxLayout(widget_requirements)
        layout.setContentsMargins(30, 5, 30, 5)
        layout.addWidget(envLabel)
        layout.addStretch(1)
        layout.addWidget(self.spinner_requirements)
        layout.addWidget(self.button_requirements)
        self.card_requirements.addWidget(widget_requirements)

        self.card_generate_code = SettingGroupCard(FluentIcon.SPEED_OFF, "Generate Code", "",
                                                  self.scrollAreaWidgetContents)
        self.gridLayout1.addWidget(self.card_generate_code, 3, 0, 1, 1)

        widget_generate_code_type = QWidget(self.card_generate_code)
        envLabel = BodyLabel("类型")
        self.comboBox_generate_code_type = ComboBox(self.card_generate_code)
        self.comboBox_generate_code_type.addItems(SETTINGS["other"]["project_types"])
        layout = QHBoxLayout(widget_generate_code_type)
        layout.setContentsMargins(30, 5, 30, 5)
        layout.addWidget(envLabel)
        layout.addStretch(1)
        layout.addWidget(self.comboBox_generate_code_type)
        self.card_generate_code.addWidget(widget_generate_code_type)

        widget_generate_code = QWidget(self.card_generate_code)
        envLabel = BodyLabel("UI 文件")
        self.spinner_generate_code = GifLabel(self.card_requirements)
        self.spinner_generate_code.setGif(APPGIF.LOADING.path())
        self.spinner_generate_code.setFixedSize(30, 30)
        self.spinner_generate_code.hide()
        self.button_filepath_ui = FilePathSelector(self.card_generate_code)
        self.button_filepath_ui.setFileTypes("*.ui")
        self.button_filepath_ui.setFixedWidth(200)
        self.button_generate_code = PrimaryDropDownPushButton(FluentIcon.MAIL, '操作')
        menu = RoundMenu(parent=self.button_generate_code)
        menu.addAction(Action(FluentIcon.BASKETBALL, '编译', triggered=self.generate_code_compile))
        menu.addAction(Action(FluentIcon.ALBUM, '生成', triggered=self.generate_code_generate))
        self.button_generate_code.setMenu(menu)

        layout = QHBoxLayout(widget_generate_code)
        layout.setContentsMargins(30, 5, 30, 5)
        layout.addWidget(envLabel)
        layout.addStretch(1)
        layout.addWidget(self.spinner_generate_code)
        layout.addWidget(self.button_filepath_ui)
        layout.addWidget(self.button_generate_code)
        self.card_generate_code.addWidget(widget_generate_code)


        verticalSpacer = QSpacerItem(0, 1000, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.gridLayout1.addItem(verticalSpacer, 4, 0, 1, 1)

        try:
            self.configure()
        except Exception as e:
            logging.error(e)
            QMessageBox.critical(self, "初始化错误", f"请检查配置文件{str(e)}")
            raise Exception(f"请检查配置文件{str(e)}")

    def configure(self):
        if CURRENT_SETTINGS["other"]["mode"] in SETTINGS["other"]["python_env_modes"]:
            self.comboBox_mode.setCurrentText(CURRENT_SETTINGS["other"]["mode"])

        if CURRENT_SETTINGS["other"]["custom_python_path"]:
            self.button_filepath.setText(CURRENT_SETTINGS["other"]["custom_python_path"])

        if CURRENT_SETTINGS["other"]["project_type"]:
            self.comboBox_generate_code_type.setCurrentText(CURRENT_SETTINGS["other"]["project_type"])

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

    def pipreqs_install(self):
        if self.pipreqs("pipreqs_install", "pipreqs"):
            Message.info("提示", "安装中，请稍后", self)

    def pipreqs_upgrade(self):
        if self.pipreqs("pipreqs_upgrade", "pipreqs"):
            Message.info("提示", "更新中，请稍后", self)

    def pipreqs_uninstall(self):
        if self.pipreqs("pipreqs_uninstall", "pipreqs"):
            Message.info("提示", "卸载中，请稍后", self)

    def pipreqs(self, cmd, args):
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

        self.button_pipreqs.setEnabled(False)
        self.spinner_pipreqs.setState(True)
        self.spinner_pipreqs.show()

        return True

    def generate_requirements(self):
        if self.venvMangerTh.isRunning():
            Message.error("错误", "env忙碌中，请稍后重试", self)
            return

        folder = self.button_env_folder.text()
        if not folder or folder == "选择":
            Message.error("错误", "请选择项目根目录", self)
            return

        path = self.getPyPath()
        if not path:
            Message.error("错误", "python解释器获取失败", self)
            return

        with open(os.path.join(ROOT_PATH, SettingPath, "pipreqs.json"), "r") as f:
            data = json.load(f)
            Pipreqs.PIPREQS_PARAMS.clear()
            for key in data.keys():
                Pipreqs.PIPREQS_PARAMS[key] = data[key]

        cmd = PyPath.PIPREQS.path(path) + ' ' + folder + ' ' + Pipreqs().getCMD()

        self.venvMangerTh.setPyInterpreter(path)
        self.venvMangerTh.setCMD("generate_requirements", cmd)
        self.venvMangerTh.start()

        self.button_requirements.setEnabled(False)
        self.spinner_requirements.setState(True)
        self.spinner_requirements.show()

        Message.info("提示", "生成中，请稍后", self)

    def install_requirements(self):
        if self.venvMangerTh.isRunning():
            Message.error("错误", "env忙碌中，请稍后重试", self)
            return

        folder = self.button_env_folder.text()
        if not folder or folder == "选择":
            Message.error("错误", "请选择项目根目录", self)
            return

        path = self.getPyPath()
        if not path:
            Message.error("错误", "python解释器获取失败", self)
            return

        if not os.path.exists(os.path.join(folder, "requirements.txt")):
            Message.error("错误", "requirements.txt 不存在", self)
            return

        self.venvMangerTh.setPyInterpreter(path)
        self.venvMangerTh.setCMD("install_requirements", "-r", os.path.join(folder, "requirements.txt"))
        self.venvMangerTh.start()

        self.button_requirements.setEnabled(False)
        self.spinner_requirements.setState(True)
        self.spinner_requirements.show()

        Message.info("提示", "安装中，请稍后", self)

    def edit_requirements(self):
        folder = self.button_env_folder.text()
        if not folder or folder == "选择":
            Message.error("错误", "请选择项目根目录", self)
            return

        file = os.path.join(folder, "requirements.txt")
        if not os.path.exists(file):
            Message.error("错误", "requirements配置文件不存在", self)
            return

        os.system(f'notepad {file}')


    def on_comboBox_mode_currentTextChanged(self, text):
        CURRENT_SETTINGS["other"]["mode"] = text

        if text == "跟随项目":
            self.widget_env.hide()
            self.widget_env_project.hide()
        elif text == "跟随全局":
            self.widget_env.hide()
            self.widget_env_project.show()
        elif text == "独立模式":
            self.widget_env.show()
            self.widget_env_project.show()
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
            CURRENT_SETTINGS["other"]["custom_python_path"] = ""
            write_config()

    def on_button_pipreqs_edit_clicked(self):
        if not os.path.exists(os.path.join(ROOT_PATH, SettingPath, "pipreqs.json")):
            Message.error("错误", "pipreqs配置文件不存在", self)
            return

        os.system(f'notepad {os.path.join(ROOT_PATH, SettingPath, "pipreqs.json")}')

    def generate_code_compile(self):
        if not self.button_filepath_ui.text():
            Message.error("错误", "UI文件不能为空", self)
            return

        path = self.getPyPath()
        if not path:
            Message.error("错误", "python解释器获取失败", self)
            return False
        cmd = ''
        if self.comboBox_generate_code_type.currentText() == "PySide2":
            cmd = PyPath.PYSIDE6_UIC.path(path)
        elif self.comboBox_generate_code_type.currentText() == "PySide6":
            cmd = PyPath.PYSIDE6_UIC.path(path)
        elif self.comboBox_generate_code_type.currentText() == "PyQt5":
            cmd = PyPath.PYQT5_UIC.path(path)
        elif self.comboBox_generate_code_type.currentText() == "PyQt6":
            cmd = PyPath.PYQT6_UIC.path(path)
        (filePath, fileName) = os.path.split(self.button_filepath_ui.text())
        outFile = os.path.join(filePath, 'Ui_' + fileName.replace('ui', 'py'))

        self.venvMangerTh.setPyInterpreter(path)
        self.venvMangerTh.setCMD("generate_code", cmd, self.button_filepath_ui.text(), '-o', outFile)
        self.venvMangerTh.start()

        self.button_generate_code.setEnabled(False)
        self.spinner_generate_code.setState(True)
        self.spinner_generate_code.show()

        Message.info("提示", "生成中，请稍后", self)

    def generate_code_generate(self):
        if not self.button_filepath_ui.text():
            Message.error("错误", "UI文件不能为空", self)
            return

        path = self.getPyPath()
        if not path:
            Message.error("错误", "python解释器获取失败", self)
            return False

        project = {
            "type": self.comboBox_generate_code_type.currentText(),
            "interpreter": path
        }

        self.spinner_generate_code.setState(True)
        self.spinner_generate_code.show()
        dialog = GenerateCodeDialog(self.button_filepath_ui.text(), project)
        dialog.setWindowIcon(QIcon(UI_CONFIG["logoPath"]))
        dialog.show()
        self.spinner_generate_code.setState(False)
        self.spinner_generate_code.hide()

    def receive_VMresult(self,  cmd, result):
        logging.debug(f"receive_VMresult: {cmd}, {result}")
        if cmd == "init":
            pass
        elif "py_version" in cmd:
            if not result[0]:
                Message.error("解释器错误", result[1], self)
                return
            self.label_ver.setText("版本: " + result[1].strip('\n'))
            CURRENT_SETTINGS["other"]["custom_python_path"] = self.button_filepath.text()
            write_config()
        elif "pipreqs" in cmd:
            self.button_pipreqs.setEnabled(True)
            self.spinner_pipreqs.setState(False)
            self.spinner_pipreqs.hide()

            if not result[0]:
                Message.error("错误", result[1], self)
                return
            if "install" in cmd:
                Message.info("提示", "安装成功", self)
            elif "upgrade" in cmd:
                Message.info("提示", "更新成功", self)
            elif "uninstall" in cmd:
                Message.info("提示", "卸载成功", self)
        elif "requirements" in cmd:
            self.button_requirements.setEnabled(True)
            self.spinner_requirements.setState(False)
            self.spinner_requirements.hide()

            if not result[0]:
                Message.error("错误", result[1], self)
                return

            if "install" in cmd:
                Message.info("提示", "安装成功", self)
            elif "generate" in cmd:
                Message.info("提示", "生成成功", self)
        elif "generate_code" in cmd:
            self.button_generate_code.setEnabled(True)
            self.spinner_generate_code.setState(False)
            self.spinner_generate_code.hide()

            if not result[0]:
                Message.error("错误", result[1], self)
                return

            Message.info("提示", "生成成功", self)
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

    def run(self):
        cmd = self.cmd
        if cmd == "init":
            pass
        elif cmd == "py_version":
            result = self.pyI.version()
            self.signal_result.emit(cmd, result)
        elif "pipreqs" in cmd:
            if "uninstall" in cmd:
                result = self.pyI.pip("uninstall", '-y', *self.args)
            elif "install" in cmd:
                result = self.pyI.pip("install", *self.args)
            elif "upgrade" in cmd:
                result = self.pyI.pip("install", "--upgrade", *self.args)

            self.signal_result.emit(cmd, result)
        elif "generate_code" in cmd:
            result = self.pyI.cmd(self.args)
            self.signal_result.emit(cmd, result)
        elif "generate" in cmd:
            result = self.pyI.cmd(self.args[0])
            self.signal_result.emit(cmd, result)
        elif "install_requirements" in cmd:
            result = self.pyI.pip("install", *self.args)
            self.signal_result.emit(cmd, result)
        else:
            self.signal_result.emit(cmd, ["False", "未知命令"])