# -*- coding: utf-8 -*-

"""
Module implementing ToolsWidget.
"""

from PySide6.QtCore import Slot
from PySide6.QtWidgets import QWidget

from .Ui_ToolsWidget import Ui_Form

from .utils.stylesheets import StyleSheet


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
