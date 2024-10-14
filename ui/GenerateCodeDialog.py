#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author: Reiner
email: nbxlc@hotmail.com
Module implementing GenerateCodeDialog.
"""


from PySide6.QtCore import Slot, Qt, QSortFilterProxyModel, QMetaObject, QProcess, QProcessEnvironment, QRegularExpression, QSortFilterProxyModel, QSize, QCoreApplication
from PySide6.QtGui import QBrush, QColor, QStandardItem, QStandardItemModel, QFont
from PySide6.QtWidgets import QWidget, QAbstractItemView, QGridLayout, QVBoxLayout, QHBoxLayout, QFrame, QSpacerItem, QSizePolicy
import os
import contextlib
import simplejson as json

from qframelesswindow import FramelessWindow, StandardTitleBar
from qfluentwidgets import InfoBar, InfoBarPosition, FluentIcon, TreeView, CaptionLabel, ComboBox, PrimaryPushButton, LineEdit
from qfluentwidgets.components.settings.expand_setting_card import GroupSeparator, SpaceWidget, ExpandBorderWidget

from qfluentexpand.components.card.settingcard import SettingGroupCard, ExpandCard
from qfluentexpand.components.line.editor import Line

from .Ui_GenerateCodeDialog import Ui_Form
from .eric import ModuleParser
from .eric.config import getConfig

pyqtSignatureRole = Qt.ItemDataRole.UserRole + 1
pythonSignatureRole = Qt.ItemDataRole.UserRole + 2
returnTypeRole = Qt.ItemDataRole.UserRole + 3
parameterTypesListRole = Qt.ItemDataRole.UserRole + 4
parameterNamesListRole = Qt.ItemDataRole.UserRole + 5


class GenerateCodeDialog(FramelessWindow, Ui_Form):
    """
    Class documentation goes here.
    """

    DialogClasses = {
        "QDialog",
        "QWidget",
        "QMainWindow",
        "QWizard",
        "QWizardPage",
        "QDockWidget",
        "QFrame",
        "QGroupBox",
        "QScrollArea",
        "QMdiArea",
        "QTabWidget",
        "QToolBox",
        "QStackedWidget",
    }

    def __init__(self, formFile, project, parent=None):
        """
        Constructor

        @param parent reference to the parent widget (defaults to None)
        @type QWidget (optional)
        """
        super().__init__(parent)
        self.setupUi(self)

        self.formFile = formFile
        self.project = {
            "type": 'PySide6',
            "interpreter": '',
            "path": ''
        }
        self.project = project

        self.gridLayout = QGridLayout(self)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(50, 50, 50, -1)
        self.gridLayout.setSpacing(20)
        self.gridLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.initTitleBar()
        self.initWidget()

    def initTitleBar(self):
        self.setTitleBar(StandardTitleBar(self))
        # self.setTitleBar(CustomTitleBar(self))
        self.setWindowTitle("Code Generator")
        # self.titleBar.setAttribute(Qt.WA_StyledBackground)
        self.titleBar.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)

    def initWidget(self):

        self.generate_card = ExpandCard(self)
        self.gridLayout.addWidget(self.generate_card, 0, 0, 1, 1)

        widget_classname = QWidget(self.generate_card)
        envLabel = CaptionLabel("Classname")
        self.ComboBox_classname = ComboBox(self.generate_card)
        self.ComboBox_classname.setMinimumWidth(300)
        self.ComboBox_classname.activated.connect(self.on_ComboBox_classname_activated)
        layout = QHBoxLayout(widget_classname)
        layout.setContentsMargins(30, 5, 30, 5)
        layout.addWidget(envLabel)
        layout.addStretch(1)
        layout.addWidget(self.ComboBox_classname)
        self.generate_card.addWidget(widget_classname)

        widget_filename = QWidget(self.generate_card)
        envLabel = CaptionLabel("Filename")
        self.LineEdit_filename = LineEdit(self)
        self.LineEdit_filename.setMinimumWidth(300)
        self.LineEdit_filename.setReadOnly(True)
        layout = QHBoxLayout(widget_filename)
        layout.setContentsMargins(30, 5, 30, 5)
        layout.addWidget(envLabel)
        layout.addStretch(1)
        layout.addWidget(self.LineEdit_filename)
        self.generate_card.addWidget(widget_filename)

        widget_filter = QWidget(self.generate_card)
        envLabel = CaptionLabel("Filter with")
        self.LineEditor_filter = Line(self)
        self.LineEditor_filter.setMinimumWidth(300)
        self.LineEditor_filter.textChanged.connect(self.on_LineEditor_filter_textChanged)
        layout = QHBoxLayout(widget_filter)
        layout.setContentsMargins(30, 5, 30, 5)
        layout.addWidget(envLabel)
        layout.addStretch(1)
        layout.addWidget(self.LineEditor_filter)
        self.generate_card.addWidget(widget_filter)

        widget_action = QWidget(self.generate_card)
        envLabel = CaptionLabel("Action")
        self.button_new = PrimaryPushButton(self.generate_card)
        self.button_new.setText("New")
        self.button_new.clicked.connect(self.on_button_new_clicked)
        self.button_save = PrimaryPushButton(self.generate_card)
        self.button_save.setText("Save")
        self.button_save.setEnabled(False)
        self.button_save.clicked.connect(self.on_button_save_clicked)
        layout = QHBoxLayout(widget_action)
        layout.setContentsMargins(30, 5, 30, 5)
        layout.addWidget(envLabel)
        layout.addStretch(1)
        layout.addWidget(self.button_new)
        layout.addWidget(self.button_save)
        self.generate_card.addWidget(widget_action)

        self.generate_class_card = ExpandCard(self)
        self.gridLayout.addWidget(self.generate_class_card, 1, 0, 1, 1)

        widget_classname_1 = QWidget(self.generate_class_card)
        envLabel = CaptionLabel("Filter with")
        self.LineEditor_classname = Line(self)
        self.LineEditor_classname.setMinimumWidth(300)
        layout = QHBoxLayout(widget_classname_1)
        layout.setContentsMargins(30, 5, 30, 5)
        layout.addWidget(envLabel)
        layout.addStretch(1)
        layout.addWidget(self.LineEditor_classname)
        self.generate_class_card.addWidget(widget_classname_1)

        widget_filename_1 = QWidget(self.generate_class_card)
        envLabel = CaptionLabel("Filename")
        self.LineEdit_filename_1 = LineEdit(self)
        self.LineEdit_filename_1.setMinimumWidth(300)
        self.LineEdit_filename_1.setReadOnly(True)
        layout = QHBoxLayout(widget_filename_1)
        layout.setContentsMargins(30, 5, 30, 5)
        layout.addWidget(envLabel)
        layout.addStretch(1)
        layout.addWidget(self.LineEdit_filename_1)
        self.generate_class_card.addWidget(widget_filename_1)

        widget_path = QWidget(self.generate_class_card)
        envLabel = CaptionLabel("Path")
        self.LineEdit_path = LineEdit(self)
        self.LineEdit_path.setMinimumWidth(300)
        self.LineEdit_path.setReadOnly( True)
        layout = QHBoxLayout(widget_path)
        layout.setContentsMargins(30, 5, 30, 5)
        layout.addWidget(envLabel)
        layout.addStretch(1)
        layout.addWidget(self.LineEdit_path)
        self.generate_class_card.addWidget(widget_path)

        widget_action_1 = QWidget(self.generate_class_card)
        envLabel = CaptionLabel("Action")
        self.button_ok = PrimaryPushButton(self.generate_class_card)
        self.button_ok.setText("OK")
        self.button_ok.clicked.connect(self.on_button_ok_clicked)
        layout = QHBoxLayout(widget_action_1)
        layout.setContentsMargins(30, 5, 30, 5)
        layout.addWidget(envLabel)
        layout.addStretch(1)
        layout.addWidget(self.button_ok)
        self.generate_class_card.addWidget(widget_action_1)

        self.generate_class_card.hide()

        self.slotsView = TreeView(self)
        self.slotsView.setObjectName(u"slotsView")
        self.slotsView.setSortingEnabled(True)
        self.slotsView.setMinimumHeight(400)
        self.slotsView.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.slotsView.header().hide()

        self.gridLayout.addWidget(self.slotsView, 2, 0, 1, 1)

        # self.verticalSpacer = QSpacerItem(0, 1000, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        # self.gridLayout.addItem(self.verticalSpacer, 3, 0, 1, 1)

        self.configure()

    def configure(self):

        if not os.path.exists(self.formFile):
            return

        (self.formPath, self.formFullName) = os.path.split(self.formFile)
        (self.formName, _ext) = os.path.splitext(self.formFile)

        self.srcFile = "{0}{1}".format(
            self.formName, '.py'
        )

        self.slotsModel = QStandardItemModel()
        self.proxyModel = QSortFilterProxyModel()
        self.proxyModel.setDynamicSortFilter(True)
        self.proxyModel.setSourceModel(self.slotsModel)
        self.slotsView.setModel(self.proxyModel)

        # initialize some member variables
        self.__initError = False
        self.__module = None
        print("self.__module", self.srcFile)
        if os.path.exists(self.srcFile):
            with contextlib.suppress(ImportError):
                splitExt = os.path.splitext(self.srcFile)
                exts = [splitExt[1]] if len(splitExt) == 2 else None
                self.__module = ModuleParser.readModule(
                    self.srcFile, extensions=exts, caching=False
                )

        if self.__module is not None:
            self.LineEdit_filename.setText(self.srcFile)

            classesList = []
            vagueClassesList = []
            for klass in self.__module.classes.values():
                if not set(klass.super).isdisjoint(
                        self.DialogClasses
                ):
                    classesList.append(klass.name)
                else:
                    vagueClassesList.append(klass.name)
            classesList.sort()
            self.ComboBox_classname.addItems(classesList)
            if vagueClassesList:
                if classesList:
                    self.ComboBox_classname.insertSeparator(self.ComboBox_classname.count())
                self.ComboBox_classname.addItems(sorted(vagueClassesList))

        if (
            os.path.exists(self.srcFile)
            and self.__module is not None
            and self.ComboBox_classname.count() == 0
        ):
            self.__initError = True
            Message.error(
                title="Create Dialog Code",
                content=f"The file {self.srcFile} exists but does not contain any classes.",
                parent=self
            )

        self.button_save.setEnabled(self.ComboBox_classname.count() > 0)

        self.__updateSlotsModel()

    def __objectName(self):
        """
        Private method to get the object name of a form.

        @return object name
        @rtype str
        """
        objectName = ""

        output, ok = self.__runUicLoadUi("object_name")
        if ok and output:
            objectName = output

        return objectName

    def __className(self):
        """
        Private method to get the class name of a form.

        @return class name
        @rtype str
        """
        className = ""

        output, ok = self.__runUicLoadUi("class_name")
        if ok and output:
            className = output

        return className

    def __signatures(self):
        """
        Private slot to get the signatures.

        @return list of signatures
        @rtype list of str
        """
        if self.__module is None:
            return []

        signatures = []
        clsName = self.ComboBox_classname.currentText()
        if clsName:
            cls = self.__module.classes[clsName]
            for meth in cls.methods.values():
                if meth.name.startswith("on_"):
                    if meth.pyqtSignature is not None:
                        sig = ", ".join(
                            [
                                bytes(QMetaObject.normalizedType(t)).decode()
                                for t in meth.pyqtSignature.split(",")
                            ]
                        )
                        signatures.append("{0}({1})".format(meth.name, sig))
                    else:
                        signatures.append(meth.name)
        return signatures

    def __runUicLoadUi(self, command):
        """
        Private method to run the UicLoadUi.py script with the given command
        and return the output.

        @param command uic command to be run
        @type str
        @return tuple of process output and error flag
        @rtype tuple of (str, bool)
        """
        env = QProcessEnvironment.systemEnvironment()

        if self.project["type"] in ("PyQt5", "PySide2"):
            loadUi = os.path.join(os.path.dirname(__file__), "eric/uic", "UicLoadUi5.py")
        elif self.project["type"] in ("PyQt6", "E7Plugin"):
            loadUi = os.path.join(os.path.dirname(__file__), "eric/uic", "UicLoadUi6.py")
        elif self.project["type"] in ("PySide6"):
            loadUi = os.path.join(os.path.dirname(__file__), "eric/uic", "UicLoadUipy6.py")
        args = [
            loadUi,
            command,
            self.formFile,
            self.formPath,
        ]

        uicText = ""
        ok = False

        proc = QProcess()
        proc.setWorkingDirectory(self.formPath)
        proc.setWorkingDirectory(self.formPath)
        proc.setProcessEnvironment(env)
        proc.start(self.project["interpreter"], args)
        started = proc.waitForStarted(5000)
        finished = proc.waitForFinished(30000)
        if started and finished:
            output = proc.readAllStandardError()
            outText = str(output, "utf-8", "replace")
            if "@@eric_start@@" in outText:
                # it is something we sent via UicLoadUi[56].py
                outText = outText.split("@@eric_start@@")[1]
                ok = True
            elif "@@eric_error@@" in outText:
                # it is something we sent via UicLoadUi[56].py
                outText = outText.split("@@eric_error@@")[1]
                ok = False
            else:
                ok = False
            if "@@eric_end@@" in outText:
                # it is something we sent via UicLoadUi[56].py
                outText = outText.split("@@eric_end@@")[0]
            if ok:
                uicText = outText.strip()
            else:
                Message.error(
                    title="uic error",
                    content=f"There was an error loading the form {self.formFile}. error: {outText}",
                    parent=self
                )
        else:
            Message.error(
                title="uic error",
                content=f"The project specific Python interpreter {self.project['interpreter']}.ould not be started or did not finish within 30 seconds.",
                parent=self
            )

        return uicText, ok

    def __updateSlotsModel(self):
        self.LineEditor_filter.clear()

        output, ok = self.__runUicLoadUi("signatures")
        if ok and output:
            try:
                objectsList = json.loads(output.strip())

                signatureList = self.__signatures()

                self.slotsModel.clear()
                self.slotsModel.setHorizontalHeaderLabels([""])
                for objectDict in objectsList:
                    itm = QStandardItem(
                        "{0} ({1})".format(objectDict["name"], objectDict["class_name"])
                    )
                    self.slotsModel.appendRow(itm)
                    for methodDict in objectDict["methods"]:
                        itm2 = QStandardItem(methodDict["signature"])
                        itm.appendRow(itm2)

                        if self.__module is not None and (
                                methodDict["methods"][0] in signatureList
                                or methodDict["methods"][1] in signatureList
                        ):
                            itm2.setFlags(Qt.ItemFlag.ItemIsEnabled)
                            itm2.setCheckState(Qt.CheckState.Checked)
                            continue

                        itm2.setData(methodDict["pyqt_signature"], pyqtSignatureRole)
                        itm2.setData(
                            methodDict["python_signature"], pythonSignatureRole
                        )
                        itm2.setData(methodDict["return_type"], returnTypeRole)
                        itm2.setData(
                            methodDict["parameter_types"], parameterTypesListRole
                        )
                        itm2.setData(
                            methodDict["parameter_names"], parameterNamesListRole
                        )

                        itm2.setFlags(
                            Qt.ItemFlag.ItemIsUserCheckable
                            | Qt.ItemFlag.ItemIsEnabled
                            | Qt.ItemFlag.ItemIsSelectable
                        )
                        itm2.setCheckState(Qt.CheckState.Unchecked)

                self.slotsView.sortByColumn(0, Qt.SortOrder.AscendingOrder)
            except json.JSONDecodeError as err:
                Message.error(
                    title="Update Slots List",
                    content=f"The update of the slots list failed because invalid data was received. Error: {str(err)} Data: {output}",
                    parent=self
                )

    def __generateCode(self):
        """
        Private slot to generate Python code as requested by the user.
        """
        # init some variables
        sourceImpl = []
        appendAtIndex = -1
        indentStr = "    "
        slotsCode = []

        if self.__module is None:
            # new file
            try:
                if self.project["type"] == "PySide2":
                    tmplName = os.path.join(
                        getConfig(), "impl_pyside2.py.tmpl"
                    )
                elif self.project["type"] == "PySide6":
                    tmplName = os.path.join(
                        getConfig(), "impl_pyside6.py.tmpl"
                    )
                elif self.project["type"] == "PyQt5":
                    tmplName = os.path.join(
                        getConfig(), "impl_pyqt5.py.tmpl"
                    )
                elif self.project["type"] in ["PyQt6", "E7Plugin"]:
                    tmplName = os.path.join(
                        getConfig(), "impl_pyqt6.py.tmpl"
                    )
                else:
                    Message.error(
                        "Code Generation",
                        self.tr(
                            """<p>No code template file available for"""
                            """ project type "{0}".</p>"""
                        ).format(self.project["type"] ),
                        self
                    )
                    return

                print("tmplName", os.path, tmplName)
                # modify
                with open(tmplName, "r", encoding="utf-8") as tmplFile:
                    template = tmplFile.read()
            except OSError as why:
                Message.error(
                    "Code Generation",
                    self.tr(
                        """<p>Could not open the code template file"""
                        """ "{0}".</p><p>Reason: {1}</p>"""
                    ).format(tmplName, str(why)),
                    self
                )
                return

            objName = self.__objectName()
            if objName:
                template = (
                    template.replace(
                        "$FORMFILE$",
                        os.path.splitext(os.path.basename(self.formFile))[0],
                    )
                    .replace("$FORMCLASS$", objName)
                    .replace("$CLASSNAME$", self.ComboBox_classname.currentText())
                    .replace("$SUPERCLASS$", self.__className())
                )

                sourceImpl = template.splitlines(True)
                appendAtIndex = -1

                # determine indent string
                for line in sourceImpl:
                    if line.lstrip().startswith("def __init__"):
                        indentStr = line.replace(line.lstrip(), "")
                        break
        else:
            # extend existing file
            try:
                with open(self.srcFile, "r", encoding="utf-8") as srcFile:
                    sourceImpl = srcFile.readlines()
                if not sourceImpl[-1].endswith("\n"):
                    sourceImpl[-1] = "{0}{1}".format(sourceImpl[-1], "\n")
            except OSError as why:
                Message.error(
                    "Code Generation",
                    self.tr(
                        """<p>Could not open the source file "{0}".</p>"""
                        """<p>Reason: {1}</p>"""
                    ).format(self.srcFile, str(why)),
                    self
                )
                return

            cls = self.__module.classes[self.ComboBox_classname.currentText()]
            if cls.endlineno == len(sourceImpl) or cls.endlineno == -1:
                appendAtIndex = -1
                # delete empty lines at end
                while not sourceImpl[-1].strip():
                    del sourceImpl[-1]
            else:
                appendAtIndex = cls.endlineno - 1
                while not sourceImpl[appendAtIndex].strip():
                    appendAtIndex -= 1
                appendAtIndex += 1

            # determine indent string
            for line in sourceImpl[cls.lineno: cls.endlineno + 1]:
                if line.lstrip().startswith("def __init__"):
                    indentStr = line.replace(line.lstrip(), "")
                    break


        pyqtSignatureFormat = ("@Slot({0})")

        for row in range(self.slotsModel.rowCount()):
            topItem = self.slotsModel.item(row)
            for childRow in range(topItem.rowCount()):
                child = topItem.child(childRow)
                if child.checkState() == Qt.CheckState.Checked and (
                    child.flags() & Qt.ItemFlag.ItemIsUserCheckable
                    == Qt.ItemFlag.ItemIsUserCheckable
                ):
                    slotsCode.append("\n")
                    slotsCode.append(
                        "{0}{1}\n".format(
                            indentStr,
                            pyqtSignatureFormat.format(child.data(pyqtSignatureRole)),
                        )
                    )
                    slotsCode.append(
                        "{0}def {1}:\n".format(
                            indentStr, child.data(pythonSignatureRole)
                        )
                    )
                    indentStr2 = indentStr * 2
                    slotsCode.append('{0}"""\n'.format(indentStr2))
                    slotsCode.append(
                        "{0}Slot documentation goes here.\n".format(indentStr2)
                    )
                    if child.data(returnTypeRole) or child.data(parameterTypesListRole):
                        slotsCode.append("\n")
                        if child.data(parameterTypesListRole):
                            for name, type_ in zip(
                                child.data(parameterNamesListRole),
                                child.data(parameterTypesListRole),
                            ):
                                slotsCode.append(
                                    "{0}@param {1} DESCRIPTION\n".format(
                                        indentStr2, name
                                    )
                                )
                                slotsCode.append(
                                    "{0}@type {1}\n".format(indentStr2, type_)
                                )
                        if child.data(returnTypeRole):
                            slotsCode.append(
                                "{0}@returns DESCRIPTION\n".format(indentStr2)
                            )
                            slotsCode.append(
                                "{0}@rtype {1}\n".format(
                                    indentStr2, child.data(returnTypeRole)
                                )
                            )
                    slotsCode.append('{0}"""\n'.format(indentStr2))
                    slotsCode.append(
                        "{0}# {1}: not implemented yet\n".format(indentStr2, "TODO")
                    )
                    slotsCode.append(
                        "{0}raise NotImplementedError\n".format(indentStr2)
                    )

        if appendAtIndex == -1:
            sourceImpl.extend(slotsCode)
        else:
            sourceImpl[appendAtIndex:appendAtIndex] = slotsCode

        # write the new code
        # newline = None if self.project.useSystemEol() else self.project.getEolString()
        # modify
        newline = None
        fn = self.LineEdit_filename.text()
        try:
            with open(fn, "w", encoding="utf-8", newline=newline) as srcFile:
                srcFile.write("".join(sourceImpl))
            Message.success(
                "Success",
                "Generate Code Success",
                self
            )
        except OSError as why:
            Message.error(
                "Code Generation",
                self.tr(
                    """<p>Could not write the source file "{0}".</p>"""
                    """<p>Reason: {1}</p>"""
                ).format(fn, str(why)),
                self
            )
            return

    def on_ComboBox_classname_activated(self, _index):
        """
        Private slot to handle the activated signal of the classname combo.

        @param _index index of the activated item (unused)
        @type int
        """
        self.button_save.setEnabled(True)
        self.__updateSlotsModel()

    def on_LineEditor_filter_textChanged(self, text):
        """
        Private slot to handle changes of the filter text.

        @param text new filter text
        @type str
        """
        rx = QRegularExpression(
            text, QRegularExpression.PatternOption.CaseInsensitiveOption
        )
        self.proxyModel.setFilterRegularExpression(rx)

    def on_button_new_clicked(self):
        self.generate_class_card.show()
        self.button_new.setEnabled(False)

        path, file = os.path.split(self.srcFile)
        objName = self.__objectName()
        if objName:
            self.LineEditor_classname.setText(objName)
            self.LineEdit_filename_1.setText(file)
            self.LineEdit_path.setText(path)

    def on_button_ok_clicked(self):
        if not self.LineEditor_classname.text():
            Message.error(
                title="Class Name",
                content=f"ClassName cannot be empty.",
                parent=self
            )
            return

        self.ComboBox_classname.clear()
        self.ComboBox_classname.addItem(self.LineEditor_classname.text())
        self.LineEdit_filename.setText(self.srcFile)

        self.srcFile = os.path.join(self.LineEdit_path.text(), self.LineEdit_filename_1.text())
        self.__module = None

        self.button_save.setEnabled(self.ComboBox_classname.count() > 0)

        # self.generate_class_card.hide()
        self.button_new.setEnabled(True)

    def on_button_save_clicked(self):
        self.__generateCode()



class Message():
    def __init__(self):
        pass

    @staticmethod
    def info(title, content, parent, isClosable=True, duration=10000, position=InfoBarPosition.BOTTOM):
        InfoBar.info(
            title=title,
            content=content,
            orient=Qt.Orientation.Vertical,  # 内容太长时可使用垂直布局
            isClosable=isClosable,
            position=position,
            duration=duration,
            parent=parent
        )

    @staticmethod
    def success(title, content, parent, isClosable=True, duration=10000, position=InfoBarPosition.BOTTOM):
        InfoBar.success(
            title=title,
            content=content,
            orient=Qt.Orientation.Vertical,  # 内容太长时可使用垂直布局
            isClosable=isClosable,
            position=position,
            duration=duration,
            parent=parent
        )

    @staticmethod
    def error(title, content, parent, isClosable=True, duration=30000, position=InfoBarPosition.BOTTOM):
        InfoBar.error(
            title=title,
            content=content,
            orient=Qt.Orientation.Vertical,  # 内容太长时可使用垂直布局
            isClosable=isClosable,
            position=position,
            duration=duration,
            parent=parent
        )

    @staticmethod
    def warning(title, content, parent, isClosable=True, duration=10000, position=InfoBarPosition.BOTTOM):
        InfoBar.warning(
            title=title,
            content=content,
            orient=Qt.Orientation.Vertical,  # 内容太长时可使用垂直布局
            isClosable=isClosable,
            position=position,
            duration=duration,
            parent=parent
        )
