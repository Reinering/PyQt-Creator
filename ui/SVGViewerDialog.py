# -*- coding: utf-8 -*-

"""
Module implementing SVGViewerDialog.
"""

from PySide6.QtCore import Slot, Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QGraphicsView, QGraphicsScene, QPushButton, QHBoxLayout, QFileDialog, QGridLayout
from PySide6.QtSvgWidgets import QGraphicsSvgItem

from qframelesswindow import FramelessWindow
from qfluentwidgets import Action, FluentIcon

from .Ui_SVGViewerDialog import Ui_Form
from .utils.stylesheets import StyleSheet


class SVGViewerDialog(FramelessWindow, Ui_Form):
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
        StyleSheet.SVGVIEWER.apply(self)

        self.gridLayout.setContentsMargins(1, 25, 1, 1)

        self.gridLayout1 = QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout1.setContentsMargins(0, 0, 0, 0)
        self.gridLayout1.setSpacing(10)
        self.gridLayout1.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.CommandBar.setMinimumWidth(250)
        self.CommandBar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.CommandBar.addAction(Action(FluentIcon.ADD, '打开', triggered=lambda: self.load_svg()))
        self.CommandBar.addAction(Action(FluentIcon.MINIMIZE, '缩小', triggered=lambda: self.zoom_out()))
        self.CommandBar.addAction(Action(FluentIcon.SETTING, '放大', triggered=lambda: self.zoom_in()))
        self.CommandBar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.CommandBar.setButtonTight(False)

        # 创建 QGraphicsView 及场景
        self.view = QGraphicsView(self)
        self.scene = QGraphicsScene(self)
        self.view.setScene(self.scene)
        self.gridLayout1.addWidget(self.view, 0, 0, 1, 1)

        # SVG 图像项
        self.svg_item = None
        self.zoom_factor = 1.0  # 初始缩放比例

    def setFile(self, file_path):
        if file_path:
            # 如果已有 SVG 项目，先清除
            if self.svg_item:
                self.scene.removeItem(self.svg_item)
                self.svg_item = None

            self.svg_item = QGraphicsSvgItem(file_path)
            self.scene.addItem(self.svg_item)
            self.scene.setSceneRect(self.svg_item.boundingRect())
            self.reset_zoom()

    def load_svg(self):
        # 打开文件对话框选择 SVG 文件
        file_path, _ = QFileDialog.getOpenFileName(self, "Open SVG File", "", "SVG files (*.svg)")
        if file_path:
            # 如果已有 SVG 项目，先清除
            if self.svg_item:
                self.scene.removeItem(self.svg_item)
                self.svg_item = None

            # 创建新的 SVG 图像项并添加到场景中
            self.svg_item = QGraphicsSvgItem(file_path)
            self.scene.addItem(self.svg_item)

            # 将场景边界调整为 SVG 项目的边界
            self.scene.setSceneRect(self.svg_item.boundingRect())
            # 重置缩放
            self.reset_zoom()

    def zoom_in(self):
        # 增加缩放比例
        self.zoom_factor *= 1.2
        self.apply_zoom()

    def zoom_out(self):
        # 减小缩放比例
        self.zoom_factor /= 1.2
        self.apply_zoom()

    def reset_zoom(self):
        # 重置缩放比例
        self.zoom_factor = 1.0
        self.apply_zoom()

    def apply_zoom(self):
        # 应用缩放到视图
        if self.svg_item:
            self.view.resetTransform()  # 重置视图的变换矩阵
            self.view.scale(self.zoom_factor, self.zoom_factor)

            # 将视图中心对准 SVG 项目的中心
            svg_center = self.svg_item.boundingRect().center()
            self.view.centerOn(svg_center)
