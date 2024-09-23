# -*- coding: utf-8 -*-

"""
Module implementing ConsoleWidget.
"""

from PySide6.QtCore import Slot
from PySide6.QtWidgets import QWidget

from .Ui_ConsoleWidget import Ui_Form

from .utils.stylesheets import StyleSheet


class ConsoleWidget(QWidget, Ui_Form):
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

        self.setObjectName("console")
        StyleSheet.CONSOLE.apply(self)
