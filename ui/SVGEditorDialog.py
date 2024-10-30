# -*- coding: utf-8 -*-

"""
Module implementing SVGEditorDialog.
"""

from PySide6.QtCore import Slot, Qt, QSizeF, QRectF, QByteArray
from PySide6.QtWidgets import QWidget, QColorDialog, QFileDialog, QGraphicsScene
from PySide6.QtGui import QColor, QPainter
from PySide6.QtSvgWidgets import QGraphicsSvgItem
from PySide6.QtSvg import QSvgGenerator, QSvgRenderer
import tempfile


from qframelesswindow import FramelessWindow, StandardTitleBar
from qfluentwidgets import ColorDialog, ColorPickerButton, Action, FluentIcon, PrimaryPushSettingCard

from qfluentexpand.common.icon import APPICON
from .Ui_SVGEditorDialog import Ui_Form
from .utils.stylesheets import StyleSheet
from .utils.svg import SVGParser


class SVGEditorDialog(FramelessWindow, Ui_Form):
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
        self.gridLayout.setContentsMargins(5, 25, 5, 5)
        StyleSheet.SVGEDITOR.apply(self)

        self.CommandBar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.CommandBar.addAction(Action(FluentIcon.ADD, '打开', triggered=lambda: self.load_svg()))
        self.CommandBar.addAction(Action(FluentIcon.SAVE, '保存', triggered=lambda: self.save()))
        self.CommandBar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.CommandBar.setButtonTight(False)
        self.CommandBar.setMinimumWidth(150)

        self.card_color = PrimaryPushSettingCard(
            text="选择",
            icon=APPICON.SOURCE,
            title="颜色替换",
            content="color picker",
        )
        self.card_color.clicked.connect(self.chooseColor)
        self.verticalLayout_2.insertWidget(1, self.card_color)

        self.scene = QGraphicsScene(self)
        self.graphicsView.setScene(self.scene)
        # SVG 图像项
        self.svg_item = None
        self.zoom_factor = 1.0  # 初始缩放比例

    def load_svg(self, file_path=None):
        if not file_path:
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

            self.parser = SVGParser(file_path)

            # 创建 QSvgRenderer
            self.renderer = QSvgRenderer()
            self.renderer.load(file_path)
            self.svg_item.setSharedRenderer(self.renderer)

    def update(self):
        if self.svg_item and self.parser:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.svg') as temp_file:
                svg_bytes = QByteArray(self.parser.tostring().encode('utf-8'))
                temp_file.write(svg_bytes)
                temp_file_path = temp_file.name
            self.load_svg(temp_file_path)

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
            self.graphicsView.resetTransform()  # 重置视图的变换矩阵
            self.graphicsView.scale(self.zoom_factor, self.zoom_factor)

            # 将视图中心对准 SVG 项目的中心
            svg_center = self.svg_item.boundingRect().center()
            self.graphicsView.centerOn(svg_center)

    def chooseColor(self):
        if self.svg_item is None:
            return
        color = QColorDialog.getColor()
        if color.isValid():
            self.parser.smart_change_color(color.name())
            self.update()

        # w = ColorDialog(QColor(0, 255, 255), "Choose Color", self, enableAlpha=True)
        # w.setAttribute(Qt.WidgetAttribute.WA_CustomWhatsThis)
        # w.colorChanged.connect(lambda color: print(color.name()))
        # w.exec()

    def save(self):
        filename, _ = QFileDialog.getSaveFileName(self, "保存SVG", "", "SVG files (*.svg)")
        if filename:
            self.parser.save(filename)
            self.load_svg(filename)

    @Slot()
    def on_PushButton_zoom_in_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        # raise NotImplementedError
        self.zoom_in()

    @Slot()
    def on_PushButton_zoom_out_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        # raise NotImplementedError
        self.zoom_out()
