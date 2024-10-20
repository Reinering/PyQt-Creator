# -*- coding: utf-8 -*-

"""
Module implementing SetupToolsDocDialog.
"""

from PySide6.QtCore import Slot
from PySide6.QtWidgets import QDialog

from .Ui_SetupToolsDocDialog import Ui_Dialog


class SetupToolsDocDialog(QDialog, Ui_Dialog):
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
