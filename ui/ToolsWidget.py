# -*- coding: utf-8 -*-

"""
Module implementing ToolsWidget.
"""

from PySide6.QtCore import Slot, Qt, QTimer, QThread, Signal
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QWidget, QGridLayout
import pyautogui as auto
from pynput import mouse
import pyperclip

from qfluentwidgets import (
    ExpandGroupSettingCard,
    PrimaryPushButton, PrimaryDropDownPushButton, PushButton,
    BodyLabel, TitleLabel, CaptionLabel,
    ScrollArea,
    CardWidget, IconWidget, ComboBox,
    RoundMenu,
    Action,
    LineEdit
)
from qfluentwidgets.common.icon import isDarkTheme, FluentIconBase, FluentIconBase as FIF, FluentIcon

from qfluentexpand.components.widgets.card import (
    SettingCardWidget, PushSettingCardWidget, PrimaryPushSettingCardWidget, ComboBoxSettingCardWidget,
    FileSettingCardWidget, FolderSettingCardWidget, LineSettingCardWidget, HyperlinkCardWidget,
    MenuPSettingCardWidget
)
from qfluentexpand.components.card.settingcard import SettingGroupCard, ComboBoxSettingCard
from qfluentexpand.components.button.floatingball import FloatingBall
from qfluentexpand.icongenie.icon import QFluentIcon

from .Ui_ToolsWidget import Ui_Form
from .compoments.info import Message

from .utils.stylesheets import StyleSheet
from manage import ROOT_PATH, UI_CONFIG, SettingPath, LIBS, SETTINGS, CURRENT_SETTINGS, REQUIREMENTS_URLS

class ToolsWidget(QWidget, Ui_Form):
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

        self.setObjectName("tools")
        StyleSheet.TOOLS.apply(self)

        self.gridLayout1 = QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout1.setObjectName(u"gridLayout")
        self.gridLayout1.setContentsMargins(50, -1, 50, -1)
        self.gridLayout1.setSpacing(30)
        self.gridLayout1.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.floatingBallStatus = False
        self.floatingBallPosition = None
        self.mousePosTh = None

        self.initWidget()

    def initWidget(self):
        self.floatingBallCard = SettingGroupCard(FluentIcon.SETTING, "悬浮球设置", "",
                                        self.scrollAreaWidgetContents)
        self.gridLayout1.addWidget(self.floatingBallCard, 1, 0, 1, 1)

        self.widget_floatingBall_show = SettingCardWidget('', '悬浮球', 'floating ball', self.floatingBallCard)
        self.button_floatingBall_show = PrimaryPushButton(QFluentIcon.googleIcon("visibility"), "显示/隐藏", self.widget_floatingBall_show)
        self.button_floatingBall_show.clicked.connect(self.on_button_floatingBall_show_clicked)
        self.widget_floatingBall_show.addStretch(1)
        self.widget_floatingBall_show.addWidget(self.button_floatingBall_show)
        self.floatingBallCard.addWidget(self.widget_floatingBall_show)

        self.widget_mousePosition_show = SettingCardWidget('', '鼠标位置', 'mouse position', self.floatingBallCard)
        self.button_mousePosition_show = PrimaryPushButton(QFluentIcon.googleIcon("visibility"), "打开/关闭",
                                                          self.widget_mousePosition_show)
        self.button_mousePosition_show.clicked.connect(self.on_button_mousePosition_show_clicked)
        self.widget_mousePosition_show.addStretch(1)
        self.widget_mousePosition_show.addWidget(self.button_mousePosition_show)
        self.floatingBallCard.addWidget(self.widget_mousePosition_show)

    def on_button_floatingBall_show_clicked(self):
        if not self.floatingBallStatus:
            self.floatingBall = FloatingBall()
            width, height = auto.size()
            self.floatingBall.setGeometry(width - 200, 200, 64, 64)
            self.floatingBall.setAlpha(0.6)
            self.floatingBall.isEnabledMove = True
            self.floatingBall.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
            self.floatingBall.customContextMenuRequested.connect(self.on_floatingBall_show_context_menu)

            self.floatingBall.show()
            self.floatingBallStatus = True
        else:
            self.floatingBall.hide()
            self.floatingBallPosition = self.floatingBall.pos()
            self.floatingBallStatus = False

    def on_floatingBall_show_context_menu(self, pos):
        if hasattr(self, 'right_click_timer') and self.right_click_timer.isActive():
            # 如果计时器还在运行，说明右键点击太快，直接返回
            return

        # 启动一个短暂的计时器防止过快点击
        self.right_click_timer = QTimer(self)
        self.right_click_timer.setSingleShot(True)
        self.right_click_timer.start(300)  # 300ms 防抖时间

        self.menu = RoundMenu(parent=self)
        self.menu.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)

        self.menu.addAction(Action(FluentIcon.COPY, '开启/关闭', triggered=self.on_button_mousePosition_show_clicked))
        self.menu.addAction(Action(FluentIcon.COPY, '复制', triggered=lambda: pyperclip.copy(self.floatingBall.text())))
        self.menu.addAction(Action(FluentIcon.COPY, '隐藏', triggered=lambda: self.on_button_floatingBall_show_clicked()))

        self.menu.exec(self.floatingBall.mapToGlobal(pos))

    def receive_mousePosition(self, pos):
        if pos:
            self.floatingBall.setText(f"{pos[0]}, {pos[1]}")

    def on_button_mousePosition_show_clicked(self):
        if not self.floatingBallStatus:
            Message.error("错误", "请先打开悬浮球", self)
            return

        if not self.mousePosTh:
            self.mousePosTh = MousePositionThread()
            self.mousePosTh.signal_mousePosition.connect(self.receive_mousePosition)

        if not self.mousePosTh.isRunning():
            self.mousePosTh.start()
            Message.info("鼠标位置", "显示已打开", self)
        else:
            self.mousePosTh.stop()
            Message.info("鼠标位置", "显示已关闭", self)

    def closeEvent(self, event):
        # 窗口关闭时终止线程
        if self.mousePosTh:
            self.mousePosTh.terminate()
        super().closeEvent(event)


class MousePositionThread(QThread):

    signal_mousePosition = Signal(tuple)
    signal_mouse_clicked = Signal(tuple)

    def __init__(self):
        super().__init__()
        self.stopBool = False
        self.interv = 0.5

    def stop(self):
        self.stopBool = True

    def run(self):
        self.stopBool = False

        def on_click(x, y, button, pressed):
            # 将事件通过信号发射出去，供 PySide 主线程接收
            self.signal_mouse_clicked.emit(x, y)

        def on_move(x, y):
            # 只要鼠标移动，这个函数就会被疯狂触发
            # print(f"鼠标当前实时坐标: ({x}, {y})")
            self.signal_mousePosition.emit((x, y))

        # 启动全局监听器
        with mouse.Listener(on_move=on_move, on_click=on_click) as listener:
            listener.join()

