# -*- coding: utf-8 -*-

"""
Module implementing PyinstallerDocDialog.
"""

from PySide6.QtCore import Slot
from PySide6.QtWidgets import QDialog

from .Ui_PyinstallerDocDialog import Ui_Dialog


class PyinstallerDocDialog(QDialog, Ui_Dialog):
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

        self.TextEdit.setReadOnly(True)
