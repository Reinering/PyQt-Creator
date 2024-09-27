# -*- coding: utf-8 -*-

"""
Module implementing DocumentWidget.
"""


from PySide6.QtCore import Slot
from PySide6.QtWidgets import QWidget

from .Ui_DocumentWidget import Ui_Form
from .utils.stylesheets import StyleSheet



class DocumentWidget(QWidget, Ui_Form):
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
        self.setObjectName("document")
        StyleSheet.DOCUMENT.apply(self)
