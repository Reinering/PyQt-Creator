# -*- coding: utf-8 -*-

"""
Module implementing ProjectWidget.
"""

from PySide6.QtCore import Slot, Qt
from PySide6.QtWidgets import QWidget, QTreeWidgetItem, QGridLayout, QHBoxLayout, QVBoxLayout, QSpacerItem, QSizePolicy

from qfluentwidgets import (
    CardWidget,
    TitleLabel, CaptionLabel, BodyLabel,
    ComboBox,
    PrimaryPushButton,
    TreeWidget, IconWidget,
    CommandBar,
    Action,
    RoundMenu,
)
from qfluentwidgets.common.icon import FluentIcon

from qfluentexpand.components.card.settingcard import SettingGroupCard
from qfluentexpand.components.line.selector import FilePathSelector

from .Ui_ProjectWidget import Ui_Form
from .utils.stylesheets import StyleSheet


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
        StyleSheet.PACK.apply(self)

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

        openBtn = PrimaryPushButton(self.titleCard)
        openBtn.setText("打开")
        openBtn.setMinimumWidth(100)
        openBtn.setMinimumHeight(40)
        hBoxLayout.addWidget(openBtn, 0, Qt.AlignmentFlag.AlignRight)

    def initTree(self):
        tree = TreeWidget(self.scrollAreaWidgetContents)

        # 添加子树
        item1 = QTreeWidgetItem(['JoJo 1 - Phantom Blood'])
        # item1.addChildren([
        #     QTreeWidgetItem(['Jonathan Joestar']),
        #     QTreeWidgetItem(['Dio Brando']),
        # ])
        tree.addTopLevelItem(item1)

        # 添加子树
        item2 = QTreeWidgetItem(['JoJo 3 - Stardust Crusaders'])
        item21 = QTreeWidgetItem(['Jotaro Kujo'])
        item21.addChildren([
            QTreeWidgetItem(['空条承太郎']),
            QTreeWidgetItem(['空条蕉太狼']),
        ])
        item2.addChild(item21)
        tree.addTopLevelItem(item2)

        # 隐藏表头
        tree.setHeaderHidden(True)
        tree.setFixedSize(300, 380)

        self.gridLayout.addWidget(tree, 0, 0, 1, 1)


        menu = RoundMenu()

        # 逐个添加动作，Action 继承自 QAction，接受 FluentIconBase 类型的图标
        menu.addAction(Action(FluentIcon.COPY, '复制', triggered=lambda: print("复制成功")))
        menu.addAction(Action(FluentIcon.CUT, '剪切', triggered=lambda: print("剪切成功")))

        # 批量添加动作
        menu.addActions([
            Action(FluentIcon.PASTE, '粘贴'),
            Action(FluentIcon.CANCEL, '撤销')
        ])

        # # 添加分割线
        menu.addSeparator()

        menu.addAction(Action('全选', shortcut='Ctrl+A'))

        commandBar = CommandBar()

        # # 逐个添加动作
        # commandBar.addAction(Action(FluentIcon.ADD, '添加', triggerred=lambda: print("添加")))
        #
        # # 添加分隔符
        # commandBar.addSeparator()
        #
        # # 批量添加动作
        # commandBar.addActions([
        #     Action(FluentIcon.EDIT, '编辑', checkable=True, triggerred=lambda: print("编辑")),
        #     Action(FluentIcon.COPY, '复制'),
        #     Action(FluentIcon.SHARE, '分享'),
        # ])

        # 添加始终隐藏的动作
        commandBar.addHiddenAction(Action(FluentIcon.SCROLL, '排序', triggered=lambda: print('排序')))
        commandBar.addHiddenAction(Action(FluentIcon.SETTING, '设置', shortcut='Ctrl+S'))

        self.gridLayout1.addWidget(commandBar, 0, 0, 1, 1)

    def initWidget(self):
        self.envcard = SettingGroupCard(FluentIcon.SPEED_OFF, "环境设置", "",
                                        self.scrollAreaWidgetContents)
        widget = QWidget(self.envcard)
        iconWidget = IconWidget(FluentIcon.SPEED_OFF)
        titleLabel = BodyLabel("模式", self.envcard)
        items = ["跟随全局", "独立模式"]
        comboBox = ComboBox(self.envcard)
        comboBox.addItems(items)
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(30, 5, 30, 5)
        layout.addWidget(iconWidget)
        layout.addWidget(titleLabel)
        layout.addStretch(1)
        layout.addWidget(comboBox)
        self.envcard.addWidget(widget)

        widget = QWidget(self.envcard)
        envLabel = BodyLabel("Python 环境")
        envButton = FilePathSelector(self.envcard)
        envButton.setText("选择")
        envButton.setFileTypes("python.exe")
        envButton.setFixedWidth(200)
        envButton.setEnabled(False)
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(30, 5, 30, 5)
        layout.addWidget(envLabel)
        layout.addStretch(1)
        layout.addWidget(envButton)
        self.envcard.addWidget(widget)

        self.gridLayout1.addWidget(self.envcard, 1, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(0, 1000, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.gridLayout1.addItem(self.verticalSpacer, 2, 0, 1, 1)


