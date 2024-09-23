#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author: Reiner New
email: nbxlc@hotmail.com
"""


from PySide6.QtCore import Slot
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QTreeWidgetItem, QMenu, QApplication
import sys
import os

from qfluentwidgets import TreeWidget



class CustomTreeWidget(TreeWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # 设置列数
        # self.setColumnCount(2)
        # 设置列名
        # self.setHeaderLabels(['Directory', 'Size'])
        # 顶层条目
        # self.addTopLevelItem(QTreeWidgetItem(['Root', '0B']))

        self.contextMenu = QMenu(self)


    def addMenuItem(self, name, callback):
        action = QAction(name, self)
        action.triggered.connect(callback)
        self.contextMenu.addAction(action)

    def addDirectory(self, *args):
        item = QTreeWidgetItem(*args)
        self.addTopLevelItem(item)

    def contextMenuEvent(self, event):
        self.contextMenu.exec(event.globalPos())

    def setPath(self, path):
        for filename in os.listdir(''):
            self.addDirectory([filename, '0B'])





if __name__ == '__main__':
    app = QApplication(sys.argv)
    tree = CustomTreeWidget()
    tree.show()
    sys.exit(app.exec())