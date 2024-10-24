#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author: Reiner
email: nbxlc@hotmail.com
Module implementing ProjectWidget.
"""


from PySide6.QtCore import Slot, Signal, Qt, QPoint, QThread, QProcess, QTimer
from PySide6.QtWidgets import (
    QWidget, QTreeWidgetItem,
    QGridLayout, QHBoxLayout, QVBoxLayout,
    QSpacerItem, QSizePolicy, QSplitter,
    QFrame, QFileSystemModel,
    QFileDialog, QLabel,
    QTreeView, QMenu,
    QMessageBox
)
from PySide6.QtGui import QIcon, QAction
import os.path
import logging
import clipboard
import subprocess
from PIL import Image
from pathlib import Path

from qfluentwidgets import (
    CardWidget,
    TitleLabel, CaptionLabel, BodyLabel, StrongBodyLabel,
    ComboBox,
    PrimaryPushButton, TransparentDropDownPushButton, PrimaryDropDownPushButton,
    IconWidget, TreeView,
    CommandBar,
    Action,
    RoundMenu,
    setFont,
    MessageBox
)
from qfluentwidgets.common.icon import FluentIcon
from qfluentexpand.components.card.settingcard import SettingGroupCard
from qfluentexpand.components.line.selector import FilePathSelector
from qfluentexpand.components.label.label import GifLabel
from qfluentexpand.common.gif import APPGIF
from qfluentexpand.components.widgets.card import SettingCardWidget, ComboBoxSettingCardWidget, FileSettingCardWidget
# from qfluentexpand.components.widgets.menu import RoundMenu

from .Ui_ProjectWidget import Ui_Form
from .GenerateCodeDialog import GenerateCodeDialog
from common.wintools import findProgramPath
from .utils.stylesheets import StyleSheet
from .utils.config import write_config
from .utils.tool import startCMD
from .compoments.menu import RecentFilesMenu
from .compoments.info import Message, MessageBox as CustomMessageBox
from .compoments.tree import FileSystemModel, FilesystemModel
from common.pyenv import PyVenvManager
from common.py import PyInterpreter, PyPath
from manage import CURRENT_SETTINGS, SETTINGS, LIBS, UI_CONFIG, PAGEWidgets, IMAGE_TYPES


class ProjectWidget(QWidget, Ui_Form):
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
        self.setObjectName("project")
        StyleSheet.PROJECT.apply(self)

        self.gridLayout1 = QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout1.setContentsMargins(0, 0, 0, 0)
        self.gridLayout1.setSpacing(10)
        self.gridLayout1.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.gridLayout11 = QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout11.setContentsMargins(50, -1, 50, -1)
        # self.gridLayout11.setSpacing(30)
        self.gridLayout11.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.gridLayout1.addLayout(self.gridLayout11, 0, 0, 1, 1)


        self.gridLayout12 = QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout12.setContentsMargins(5, 5, 5, 5)
        # self.gridLayout12.setSpacing(30)
        self.gridLayout12.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.gridLayout1.addLayout(self.gridLayout12, 1, 0, 1, 1)

        self.venvMangerTh = VenvManagerThread()
        self.venvMangerTh.signal_result.connect(self.receive_VMresult)

        self.initTitle()
        self.initWidget()

    def initTitle(self):
        self.titleCard = CardWidget(self)
        self.titleCard.setMinimumHeight(200)
        self.gridLayout11.addWidget(self.titleCard, 0, 0, 1, 1)
        # self.ScrollArea.setViewportMargins(0, self.titleCard.height(), 0, 0)
        self.ScrollArea.setWidgetResizable(True)

        titleLabel = TitleLabel("Project", self)
        subtitleLabel = CaptionLabel("打开项目目录", self)

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

        horizontalSpacer = QSpacerItem(1000, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.button_project = PrimaryDropDownPushButton(FluentIcon.BRUSH, '操作', self)
        self.spinner_project = GifLabel(self.titleCard)
        self.spinner_project.setGif(APPGIF.LOADING)
        self.spinner_project.setFixedSize(30, 30)
        self.spinner_project.hide()
        hBoxLayout.addItem(horizontalSpacer)
        hBoxLayout.addWidget(self.spinner_project)
        hBoxLayout.addWidget(self.button_project)

        self.menu_project = RoundMenu(parent=self.button_project)
        self.menu_project.addAction(Action(FluentIcon.CONNECT, '打开项目', triggered=self.button_project_open))

        self.recentFilesMenu = RecentFilesMenu(FluentIcon.MORE, CURRENT_SETTINGS["project"]["recently_opened"], parent=self)
        self.menu_project.addMenu(self.recentFilesMenu)
        self.recentFilesMenu.fileSelected.connect(self.button_project_recently_open)

        self.menu_project.addAction(Action(FluentIcon.CLOSE, '关闭项目', triggered=self.button_project_close))
        self.button_project.setMenu(self.menu_project)

    def initWidget(self):
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setHandleWidth(0)
        self.gridLayout12.addWidget(splitter, 1, 0, 1, 1)

        leftFrame = QFrame(self)
        leftFrame.setObjectName("leftFrame")
        leftFrame.setFrameShape(QFrame.Shape.StyledPanel)
        splitter.addWidget(leftFrame)

        self.gridLayout111 = QGridLayout(leftFrame)
        self.gridLayout111.setContentsMargins(5, 1, 5, 1)
        # self.gridLayout111.setSpacing(30)
        self.gridLayout111.setAlignment(Qt.AlignmentFlag.AlignTop)

        hBoxLayout = QHBoxLayout(leftFrame)
        self.gridLayout111.addLayout(hBoxLayout, 0, 0, 1, 1)

        self.treeTitle = BodyLabel(leftFrame)
        self.treeTitle.setText("项目目录")
        self.treeTitle.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Ignored)
        self.treeTitle.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.treeTitle.setMinimumWidth(100)
        self.commandBar = CommandBar(leftFrame)
        self.commandBar.setMaximumWidth(50)
        hBoxLayout.addWidget(self.treeTitle)
        hBoxLayout.addStretch(1)
        hBoxLayout.addWidget(self.commandBar)

        # 添加始终隐藏的动作
        button = TransparentDropDownPushButton(self.tr('Sort'), self, FluentIcon.SCROLL)
        button.setFixedHeight(34)
        setFont(button, 12)
        self.commandBar.addWidget(button)

        self.commandBar.addHiddenActions([
            Action(FluentIcon.SETTING, self.tr('Settings')),
        ])

        self.tree = TreeView(self.scrollAreaWidgetContents)
        self.tree.setHeaderHidden(True)
        self.tree.setMinimumWidth(100)
        self.tree.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self.show_context_menu)
        self.gridLayout111.addWidget(self.tree, 1, 0, 1, 1)

        rightFrame = QFrame(self)
        rightFrame.setObjectName("rightFrame")
        rightFrame.setFrameShape(QFrame.Shape.StyledPanel)
        rightFrame.setMinimumWidth(300)
        splitter.addWidget(rightFrame)

        splitter.setSizes([200, 500])

        self.gridLayout121 = QGridLayout(rightFrame)
        self.gridLayout121.setContentsMargins(20, 20, 20, 20)
        self.gridLayout121.setSpacing(30)
        self.gridLayout121.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.envCard = SettingGroupCard(FluentIcon.SETTING, "环境设置", "python",
                                        self.scrollAreaWidgetContents)
        self.gridLayout121.addWidget(self.envCard, 0, 0, 1, 1)

        self.comboBox_mode = ComboBoxSettingCardWidget('', "模式", "", self.envCard)
        self.comboBox_mode.addItems(SETTINGS["project"]["python_env_modes"])
        self.comboBox_mode.currentTextChanged.connect(self.on_comboBox_mode_currentTextChanged)
        self.envCard.addWidget(self.comboBox_mode)

        self.widget_env = SettingCardWidget('', "Python 环境", "", self.envCard)
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

        self.card_project = SettingGroupCard(FluentIcon.SETTING, "项目设置", "",
                                             self.scrollAreaWidgetContents)
        self.gridLayout121.addWidget(self.card_project, 1, 0, 1, 1)
        self.comboBox_project_type = ComboBoxSettingCardWidget('', "类型", "", self.card_project)
        self.comboBox_project_type.addItems(SETTINGS["project"]["project_types"])
        self.card_project.addWidget(self.comboBox_project_type)

        self.verticalSpacer = QSpacerItem(0, 1000, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.gridLayout121.addItem(self.verticalSpacer)

        try:
            self.configure()
        except Exception as e:
            logging.error(e)
            QMessageBox.critical(self, "初始化错误", f"请检查配置文件{str(e)}")
            raise Exception(f"请检查配置文件{str(e)}")

    def configure(self):
        if CURRENT_SETTINGS["project"]["mode"] in SETTINGS["project"]["python_env_modes"]:
            self.comboBox_mode.setCurrentText(CURRENT_SETTINGS["project"]["mode"])

        if CURRENT_SETTINGS["project"]["custom_python_path"]:
            self.button_filepath.setText(CURRENT_SETTINGS["project"]["custom_python_path"])

    def initTree1(self, rootPath):
        self.treeTitle.setText(f"项目目录 ({rootPath})")
        fileModel = FilesystemModel()
        fileModel.setRootPath(rootPath)
        self.tree.setModel(fileModel)
        self.tree.setEditTriggers(QTreeView.EditTrigger.NoEditTriggers)
        # self.tree.setRootIndex(fileModel.index(rootPath))

        # 隐藏列
        self.tree.setColumnHidden(1, True)
        self.tree.setColumnHidden(2, True)
        self.tree.setColumnHidden(3, True)

    def initTree(self, rootPath):
        self.treeTitle.setText(f"项目目录 ({rootPath})")
        fileModel = QFileSystemModel()
        fileModel.setRootPath(rootPath)
        self.tree.setModel(fileModel)
        self.tree.setRootIndex(fileModel.index(rootPath))
        self.tree.setEditTriggers(QTreeView.EditTrigger.NoEditTriggers)

        # 隐藏列
        self.tree.setColumnHidden(1, True)
        self.tree.setColumnHidden(2, True)
        self.tree.setColumnHidden(3, True)

        self.menu = RoundMenu(self)
        self.menu_opened = False

    def on_menu_aboutToHide(self):
        print("on_menu_aboutToHide")
        self.menu_opened = True

    def show_context_menu(self, pos):
        if self.tree.model() is None:
            return

        if hasattr(self, 'right_click_timer') and self.right_click_timer.isActive():
            # 如果计时器还在运行，说明右键点击太快，直接返回
            return

        # 启动一个短暂的计时器防止过快点击
        self.right_click_timer = QTimer(self)
        self.right_click_timer.setSingleShot(True)
        self.right_click_timer.start(300)  # 300ms 防抖时间

        self.menu = RoundMenu(self)
        self.menu.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        try:
            index = self.tree.indexAt(pos)

            if not index.isValid():
                self.menu.addAction(
                    Action(FluentIcon.COPY, '新建文件', triggered=lambda: self.tree_open_newfile()))
                self.menu.addAction(
                    Action(FluentIcon.COPY, '新建文件夹', triggered=lambda: self.tree_open_newfolder()))
            else:
                # 获取文件路径
                try:
                    file_path = self.tree.model().filePath(index)
                except Exception as e:
                    logging.error(e)
                    return

                # 批量添加动作
                # menu.addActions([
                #     Action(FluentIcon.COPY, '复制', triggered=lambda path=file_path: self.tree_setup_pack(file_path)),
                #     Action(FluentIcon.PASTE, '粘贴', triggered=lambda path=file_path: self.tree_setup_pack(file_path)),
                # ])

                self.menu.addAction(
                    Action(FluentIcon.COPY, '打开所在目录', triggered=lambda path=file_path: self.tree_open_path(file_path)))
                self.menu.addAction(
                    Action(FluentIcon.COPY, '复制路径', triggered=lambda path=file_path: self.tree_copy_path(file_path)))

                if os.path.isfile(file_path):
                    # 添加分割线
                    self.menu.addSeparator()
                    (filepath, filename) = os.path.split(file_path)
                    (name, suffix) = os.path.splitext(file_path)
                    if filename == "setup.py":
                        self.menu.addAction(Action(FluentIcon.ADD, '操作', triggered=lambda path=file_path: self.tree_setup_action(file_path)))
                    elif filename == "requirements.txt":
                        self.menu.addAction(Action(FluentIcon.ADD, '操作', triggered=lambda path=file_path: self.tree_requirements_action(file_path)))

                    if suffix == ".ui":
                        self.menu.addAction(Action(FluentIcon.ADD_TO, 'designer', triggered=lambda path=file_path: self.tree_ui_designer(file_path)))

                        # submenu_designer = RoundMenu("使用designer打开", self)
                        # submenu_designer.setIcon(FluentIcon.PASTE)
                        # menu.addMenu(submenu_designer)
                        # submenu_designer.addAction(Action(FluentIcon.PASTE, 'designer', triggered=lambda path=file_path: self.tree_ui_designer(file_path)))

                        self.menu.addAction(Action(FluentIcon.CODE, '编译', triggered=lambda path=file_path: self.tree_ui_complie(file_path)))
                        self.menu.addAction(Action(FluentIcon.CODE, '生成代码', triggered=lambda path=file_path: self.tree_generate_code(file_path)))
                    elif suffix == ".qrc":
                        self.menu.addAction(Action(FluentIcon.CODE, '编译', triggered=lambda path=file_path: self.tree_qrc_complie(file_path)))
                    elif suffix == ".whl":
                        self.menu.addAction(Action(FluentIcon.ADD, '操作', triggered=lambda path=file_path: self.tree_whl_action(file_path)))
                    elif suffix in IMAGE_TYPES:
                        self.menu.addAction(Action(FluentIcon.EDIT, '查看', triggered=lambda path=file_path: self.tree_image_action(file_path)))
                    else:
                        self.menu.addAction(Action(FluentIcon.EDIT, '编辑', triggered=lambda path=file_path: self.tree_edit(file_path)))
                        if suffix == ".py":
                            self.menu.addAction(Action(FluentIcon.PRINT, '运行', triggered=lambda path=file_path: self.tree_py_run(file_path)))
                            self.menu.addAction(Action(FluentIcon.ROBOT, '打包成exe', triggered=lambda path=file_path: self.tree_py_pack(file_path)))
                else:
                    # menu.addSeparator()
                    pass

                # menu.addAction(Action(FluentIcon.COPY, '通过vscode打开', triggered=lambda path=file_path: self.tree_open_vscode(file_path)))
                # menu.addAction(Action(FluentIcon.CUT, '通过pycharm打开', triggered=lambda path=file_path: self.tree_open_pycharm(file_path)))
                self.menu.addSeparator()

                if os.path.isdir(file_path):
                    self.menu.addAction(Action(FluentIcon.FILTER, '新建文件', triggered=lambda path=file_path: self.tree_open_newfile(file_path)))
                    self.menu.addAction(Action(FluentIcon.FOLDER, '新建文件夹', triggered=lambda path=file_path: self.tree_open_newfolder(file_path)))

                self.menu.addAction(Action(FluentIcon.PASTE, '重命名', triggered=lambda path=file_path: self.tree_rename(file_path)))
                self.menu.addAction(Action(FluentIcon.DELETE, '删除', triggered=lambda path=file_path: self.tree_open_del(file_path)))
            self.menu.exec(self.tree.viewport().mapToGlobal(pos))       # 同步
            # menu.popup(self.tree.viewport().mapToGlobal(pos))         # 异步
        except Exception as e:
            logging.error(e)
            print(e)
        except BaseException as e:
            logging.error("未捕获的严重异常: %s", e)
            # raise  # 重新抛出严重异常，避免程序静默失败

    def show_context_menu1(self, pos):
        if self.tree.model() is None:
            return

        try:
            index = self.tree.indexAt(pos)
            menu = QMenu(self)

            if not index.isValid():
                menu.addAction(
                    QAction('新建文件', self))
                menu.addAction(
                    QAction('新建文件夹', self))
            else:
                # 获取文件路径
                try:
                    file_path = self.tree.model().filePath(index)
                except Exception as e:
                    logging.error(e)
                    return

                # 批量添加动作
                # menu.addActions([
                #     Action(FluentIcon.PASTE, '复制', triggered=lambda path=file_path: self.tree_setup_pack(file_path)),
                #     Action(FluentIcon.PASTE, '粘贴', triggered=lambda path=file_path: self.tree_setup_pack(file_path)),
                # ])

                menu.addAction(
                    QAction('打开所在目录', self))
                menu.addAction(
                    QAction('复制路径', self))

                if os.path.isfile(file_path):
                    # 添加分割线
                    menu.addSeparator()
                    (filepath, filename) = os.path.split(file_path)
                    (name, suffix) = os.path.splitext(file_path)
                    if filename == "setup.py":
                        menu.addAction(QAction('操作', self))
                    elif filename == "requirements.txt":
                        menu.addAction(QAction('操作', self))
                    if suffix == ".ui":
                        menu.addAction(QAction('designer', self))
                        menu.addAction(QAction('编译', self))
                        menu.addAction(QAction('生成代码', self))
                    elif suffix == ".qrc":
                        menu.addAction(QAction('编译', self))
                    elif suffix == ".whl":
                        menu.addAction(QAction('操作', self))
                    elif suffix in IMAGE_TYPES:
                        menu.addAction(QAction('查看', self))
                    else:
                        menu.addAction(QAction('编辑', self))
                        if suffix == ".py":
                            menu.addAction(QAction('运行', self))
                            menu.addAction(QAction('打包成exe', self))
                else:
                    # menu.addSeparator()
                    pass

                menu.addSeparator()

                if os.path.isdir(file_path):
                    menu.addAction(QAction('新建文件', self))
                    menu.addAction(QAction('新建文件夹', self))

                menu.addAction(QAction('重命名', self))
                menu.addAction(QAction('删除', self))
            menu.exec(self.tree.viewport().mapToGlobal(pos))
            # menu.popup(self.tree.viewport().mapToGlobal(pos))
        except Exception as e:
            logging.error(e)
            print(e)
        except BaseException as e:
            logging.error("未捕获的严重异常: %s", e)
            raise  # 重新抛出严重异常，避免程序静默失败
        finally:
            # 确保菜单被正确清理
            if menu:
                menu.deleteLater()

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

        return path

    def setEnviron(self, **kwargs):
        for key, value in kwargs.items():
            os.environ[key] = value

    def button_project_open(self):
        try:
            folderPath = QFileDialog.getExistingDirectory(self, u"选择目录", "/",
                                                          QFileDialog.Option.ShowDirsOnly)
            if not folderPath:
                return

            self.recentFilesMenu.addFile(folderPath)
            self.initTree(folderPath)
            write_config()
        except Exception as e:
            print(e)

    def button_project_recently_open(self, folderPath):
        self.recentFilesMenu.addFile(folderPath)
        write_config()
        self.initTree(folderPath)

    def button_project_close(self):
        self.tree.setModel(None)
        self.treeTitle.setText("项目目录")

    def on_comboBox_mode_currentTextChanged(self, text):
        CURRENT_SETTINGS["project"]["mode"] = text

        if text == "跟随全局":
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
            CURRENT_SETTINGS["project"]["custom_python_path"] = ""
            write_config()

    def on_button_teminal_clicked(self):
        path = self.getPyPath()
        if not path:
            Message.error("错误", "python解释器获取失败", self)
            return
        if not Path(path).is_absolute():
            path = str(Path(path).absolute())

        startCMD(path)

    def tree_edit(self, file_path):
        try:
            if CURRENT_SETTINGS["settings"]["editor"]:
                subprocess.run([CURRENT_SETTINGS["settings"]["editor"], file_path])
            else:
                subprocess.run(["notepad", file_path])
        except Exception as e:
            print(e)
            logging.error(e)
            Message.error("错误", "编辑器打开失败", self)

    def tree_py_run(self, file_path):

        path = self.getPyPath()
        if not path:
            Message.error("错误", "python解释器获取失败", self)
            return False

        (filepath, filename) = os.path.split(file_path)

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

        # self.venvMangerTh.setPyInterpreter(path)
        # self.venvMangerTh.setEnviron(PYTHONPATH=(';').join(pythonPath))
        # self.venvMangerTh.setCMD("py_run", file_path)
        # self.venvMangerTh.start()
        #
        # self.spinner_project.setState(True)
        # self.spinner_project.show()

        self.setEnviron(PYTHONPATH=(';').join(pythonPath))
        subprocess.Popen([path, file_path],
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)

        Message.info("提示", "开始运行", self)

    def tree_py_pack(self, file_path):
        PAGEWidgets["pack"].setMainFile(file_path)
        PAGEWidgets["main"].forward("Pack")

    def tree_ui_designer(self, file_path):
        PAGEWidgets["designer"].setUIFile(file_path)
        PAGEWidgets["main"].forward("Designer")

    def tree_ui_complie(self, file_path):
        if not file_path:
            Message.error("错误", "UI文件不能为空", self)
            return

        path = self.getPyPath()
        if not path:
            Message.error("错误", "python解释器获取失败", self)
            return False
        cmd = ''
        if self.comboBox_project_type.currentText() == "PySide2":
            cmd = PyPath.PYSIDE6_UIC.path(path)
        elif self.comboBox_project_type.currentText() == "PySide6":
            cmd = PyPath.PYSIDE6_UIC.path(path)
        elif self.comboBox_project_type.currentText() == "PyQt5":
            cmd = PyPath.PYQT5_UIC.path(path)
        elif self.comboBox_project_type.currentText() == "PyQt6":
            cmd = PyPath.PYQT6_UIC.path(path)
        (filePath, fileName) = os.path.split(file_path)
        outFile = os.path.join(filePath, 'Ui_' + fileName.replace('ui', 'py'))

        self.venvMangerTh.setPyInterpreter(path)
        self.venvMangerTh.setCMD("generate_code", cmd, file_path, '-o', outFile)
        self.venvMangerTh.start()

        self.spinner_project.setState(True)
        self.spinner_project.show()

    def tree_generate_code(self, file_path):
        if not file_path:
            Message.error("错误", "UI文件不能为空", self)
            return

        path = self.getPyPath()
        if not path:
            Message.error("错误", "python解释器获取失败", self)
            return False

        project = {
            "type": self.comboBox_project_type.currentText(),
            "interpreter": path
        }

        self.spinner_project.setState(True)
        self.spinner_project.show()
        dialog = GenerateCodeDialog(file_path, project)
        dialog.setWindowIcon(QIcon(UI_CONFIG["logoPath"]))
        dialog.show()
        self.spinner_project.setState(False)
        self.spinner_project.hide()

    def tree_qrc_complie(self, file_path):
        if not file_path:
            Message.error("错误", "UI文件不能为空", self)
            return

        path = self.getPyPath()
        if not path:
            Message.error("错误", "python解释器获取失败", self)
            return False

        cmd = ''
        if self.comboBox_project_type.currentText() == "PySide2":
            cmd = PyPath.PYSIDE6_RCC.path(path)
        elif self.comboBox_project_type.currentText() == "PySide6":
            cmd = PyPath.PYSIDE6_RCC.path(path)
        elif self.comboBox_project_type.currentText() == "PyQt5":
            cmd = PyPath.PYQT5_RCC.path(path)
        elif self.comboBox_project_type.currentText() == "PyQt6":
            Message.info("提示", "PyQt6没有rcc,使用PySide6的rcc进行编译", self)
            cmd = PyPath.PYSIDE6_RCC.path(path)
        (filePath, fileName) = os.path.split(file_path)
        (file_name, suffix) = os.path.splitext(fileName)
        outFile = os.path.join(filePath, file_name + '_rc.py')

        self.venvMangerTh.setPyInterpreter(path)
        self.venvMangerTh.setCMD("compile_rcc", cmd, file_path, '-o', outFile, self.comboBox_project_type.currentText())
        self.venvMangerTh.start()

        self.spinner_project.setState(True)
        self.spinner_project.show()

    def tree_copy_path(self, file_path):
        clipboard.copy(file_path)
        Message.info("提示", "复制成功", self)

    def tree_whl_action(self, file_path):
        PAGEWidgets["other"].setWHLFile(file_path)
        PAGEWidgets["main"].forward("Other")

    def tree_setup_action(self, file_path):
        PAGEWidgets["pack"].setSetupFile(file_path)
        PAGEWidgets["main"].forward("Pack")

    def tree_open_path(self, file_path):
        if os.path.isfile(file_path):
            (filePath, fileName) = os.path.split(file_path)
            os.startfile(filePath)
        else:
            os.startfile(file_path)

    def tree_open_vscode(self, file_path):
        exe = findProgramPath("vscode.exe")
        subprocess.run("code")

    def tree_open_pycharm(self, file_path):
        exe = findProgramPath("pycharm.exe")
        subprocess.run([exe, file_path])

    def tree_open_newfile(self, file_path=None):
        if not file_path:
            filepath = self.tree.model().rootPath()
        else:
            (filepath, filename) = os.path.split(file_path)

        dialog = CustomMessageBox("新建文件", "请输入文件名", "文件名不正确", self)
        if dialog.exec():
            filename = dialog.text()
            if filename:
                with open(os.path.join(filepath, filename), 'w', encoding='utf-8') as f:
                    f.write("")
                logging.info(f"新建文件 {filename}")
                Message.info("提示", "新建成功", self)

    def tree_open_newfolder(self, file_path=None):
        if not file_path:
            filepath = self.tree.model().rootPath()
        else:
            (filepath, filename) = os.path.split(file_path)

        dialog = CustomMessageBox("新建文件夹", "请输入文件夹名", "文件夹名不正确", self)
        if dialog.exec():
            folder = dialog.text()
            print(folder)
            if folder:
                os.mkdir(os.path.join(filepath, folder))
                logging.info(f"新建文件夹 {folder}")
                Message.info("提示", "新建成功", self)

    def tree_open_del(self, file_path):
        dialog = MessageBox("警告", f"确认删除 {file_path}？", self)
        dialog.yesButton.setText("确认")
        dialog.cancelButton.setText("取消")

        if dialog.exec():
            print('确认')
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                os.rmdir(file_path)
            else:
                pass
            logging.info(f"删除 {file_path}")
            Message.info("提示", "删除成功", self)
        else:
            print('取消')

    def tree_requirements_action(self, file_path):
        PAGEWidgets["other"].setRequirementsFile(file_path)
        PAGEWidgets["main"].forward("Other")

    def tree_rename(self, file_path):
        (filePath, fileName) = os.path.split(file_path)
        dialog = CustomMessageBox("重命名", "请输入新文件名", "文件名不正确", self)
        dialog.setText(fileName)
        if dialog.exec():
            newFileName = dialog.text()
            if newFileName:
                newFilePath = os.path.join(filePath, newFileName)
                os.rename(file_path, newFilePath)
                logging.info(f"重命名 {fileName} -> {newFileName}")
                Message.info("提示", "重命名成功", self)

    def tree_image_action(self, file_path):
        img = Image.open(file_path)
        img.show()

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
            CURRENT_SETTINGS["project"]["custom_python_path"] = self.button_filepath.text()
            write_config()
        elif "generate_code" in cmd or "compile_rcc" in cmd:
            self.spinner_project.setState(False)
            self.spinner_project.hide()

            if not result[0]:
                Message.error("错误", output, self)
                return

            Message.info("提示", "生成成功", self)
        elif "designer" in cmd:
            if not result[0]:
                Message.error("错误", output, self)
                return
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
        elif "generate_code" in cmd:
            result = self.pyI.cmd(self.args)
            self.signal_result.emit(cmd, result)
        elif "generate" in cmd:
            result = self.pyI.cmd(self.args[0])
            self.signal_result.emit(cmd, result)
        elif "compile_rcc" in cmd:
            result = self.pyI.cmd(self.args[:-1])
            if result[0] and "PyQt6" in self.args[-2]:
                with open(self.args[-2], 'r', encoding='utf-8') as f:
                    text = f.read()
                    new_text = text.replace("PySide6", "PyQt6")
                    with open(self.args[-2], 'w', encoding='utf-8') as f1:
                        f1.write(new_text)
            self.signal_result.emit(cmd, result)
        elif "py_run" in cmd:
            result = self.pyI.py(self.args[0])
            self.signal_result.emit(cmd, result)
        elif cmd == "designer":
            result = self.pyI.cmd(self.args)
            self.signal_result.emit(cmd, result)
        elif cmd == "designer_plugin":
            result = self.pyI.py_popen(self.args)
            self.signal_result.emit(cmd, result)
        else:
            self.signal_result.emit(cmd, ["False", "未知命令"])