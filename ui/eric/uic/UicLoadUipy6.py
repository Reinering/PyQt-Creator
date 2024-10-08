# -*- coding: utf-8 -*-

# Copyright (c) 2011 - 2024 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module to get the object name, class name or signatures of a Qt form (*.ui).
"""

import contextlib
import json
import os
import sys
import xml.etree.ElementTree  # secok


def _printout(dataString):
    """
    Function to print the given string as output to sys.stderr with a guard string.

    @param dataString string to be printed
    @type str
    """
    print("@@eric_start@@{0}@@eric_end@@".format(dataString), file=sys.stderr)


def _printerr(dataString):
    """
    Function to print the given string as error to sys.stdoerr with a guard string.

    @param dataString string to be printed
    @type str
    """
    print("@@eric_error@@{0}@@eric_end@@".format(dataString), file=sys.stderr)


try:
    from PySide6 import QtUiTools
    from PySide6.QtCore import QByteArray, QMetaMethod, QFile
    from PySide6.QtGui import QAction
    from PySide6.QtWidgets import QApplication, QWidget
except ModuleNotFoundError:
    _printout("PySide6 could not be found.")
    sys.exit(1)
except ImportError as err:
    _printerr("PySide6 could not be imported. Issue: {0}".format(str(err)))
    sys.exit(1)

with contextlib.suppress(ImportError):
    from PySide6 import QtWebEngineWidgets  # __IGNORE_WARNING__

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
# add the eric package directory


def objectName1(formFile, projectPath):
    """
    Function to get the object name of a form.

    @param formFile file name of the form
    @type str
    @param projectPath directory name of the project
    @type str
    """
    sys.path.append(projectPath)

    _app = QApplication([])  # __IGNORE_WARNING__
    try:
        loader = QtUiTools.QUiLoader()
        with open(formFile, 'r') as file:
            dlg = loader.load(file)
        _printout(dlg.objectName())
        sys.exit(0)
    except (AttributeError, ImportError, xml.etree.ElementTree.ParseError) as err:
        _printerr(str(err))
        sys.exit(1)


def objectName(formFile, projectPath):
    """
    Function to get the object name of a form.

    @param formFile file name of the form
    @type str
    @param projectPath directory name of the project
    @type str
    """
    sys.path.append(projectPath)

    _app = QApplication([])  # __IGNORE_WARNING__
    try:
        loader = QtUiTools.QUiLoader()
        file = QFile(formFile)  # 使用 QFile 处理文件
        if not file.open(QFile.OpenModeFlag.ReadOnly):
            raise IOError(f"Unable to open {formFile}")
        dlg = loader.load(file)  # 将 QFile 对象传递给 load 函数
        file.close()

        _printout(dlg.objectName())
        sys.exit(0)
    except (AttributeError, ImportError, xml.etree.ElementTree.ParseError) as err:
        _printerr(str(err))
        sys.exit(1)


def className(formFile, projectPath):
    """
    Function to get the class name of a form.

    @param formFile file name of the form
    @type str
    @param projectPath directory name of the project
    @type str
    """
    sys.path.append(projectPath)

    _app = QApplication([])  # __IGNORE_WARNING__
    try:
        loader = QtUiTools.QUiLoader()
        file = QFile(formFile)  # 使用 QFile 处理文件
        if not file.open(QFile.OpenModeFlag.ReadOnly):
            raise IOError(f"Unable to open {formFile}")
        dlg = loader.load(file)  # 将 QFile 对象传递给 load 函数
        file.close()
        _printout(dlg.metaObject().className())


        sys.exit(0)
    except (AttributeError, ImportError, xml.etree.ElementTree.ParseError) as err:
        _printerr(str(err))
        sys.exit(1)


def __mapType(type_):
    """
    Private function to map a type as reported by Qt's meta object to the
    correct Python type.

    @param type_ type as reported by Qt
    @type QByteArray or bytes
    @return mapped Python type
    @rtype str
    """
    mapped = bytes(type_).decode()

    # I. always check for *
    mapped = mapped.replace("*", "")

    # 1. check for const
    mapped = mapped.replace("const ", "")

    # 2. replace QString and QStringList
    mapped = mapped.replace("QStringList", "list").replace("QString", "str")

    # 3. replace double by float
    mapped = mapped.replace("double", "float")

    return mapped


def signatures(formFile, projectPath):
    """
    Function to get the signatures of form elements.

    @param formFile file name of the form
    @type str
    @param projectPath directory name of the project
    @type str
    """
    sys.path.append(projectPath)

    objectsList = []

    _app = QApplication([])  # __IGNORE_WARNING__
    try:
        loader = QtUiTools.QUiLoader()
        file = QFile(formFile)  # 使用 QFile 处理文件
        if not file.open(QFile.OpenModeFlag.ReadOnly):
            raise IOError(f"Unable to open {formFile}")
        dlg = loader.load(file)  # 将 QFile 对象传递给 load 函数
        objects = dlg.findChildren(QWidget) + dlg.findChildren(QAction)
        for obj in objects:
            name = obj.objectName()
            if not name or name.startswith("qt_"):
                # ignore un-named or internal objects
                continue

            metaObject = obj.metaObject()
            objectDict = {
                "name": name,
                "class_name": metaObject.className(),
                "methods": [],
            }

            for index in range(metaObject.methodCount()):
                metaMethod = metaObject.method(index)
                if metaMethod.methodType() == QMetaMethod.MethodType.Signal:
                    signatureDict = {
                        "signature": "on_{0}_{1}".format(
                            name, bytes(metaMethod.methodSignature()).decode()
                        ),
                        "methods": [
                            "on_{0}_{1}".format(
                                name,
                                bytes(metaMethod.methodSignature())
                                .decode()
                                .split("(")[0],
                            )
                        ],
                    }
                    signatureDict["methods"].append(
                        "{0}({1})".format(
                            signatureDict["methods"][-1],
                            ", ".join(
                                [__mapType(t) for t in metaMethod.parameterTypes()]
                            ),
                        )
                    )

                    returnType = __mapType(metaMethod.typeName().encode())
                    if returnType == "void":
                        returnType = ""
                    signatureDict["return_type"] = returnType
                    parameterTypesList = [
                        __mapType(t) for t in metaMethod.parameterTypes()
                    ]
                    signatureDict["parameter_types"] = parameterTypesList
                    pyqtSignature = ", ".join(parameterTypesList)
                    signatureDict["pyqt_signature"] = pyqtSignature

                    parameterNames = metaMethod.parameterNames()
                    if parameterNames:
                        for index in range(len(parameterNames)):
                            if not parameterNames[index]:
                                parameterNames[index] = QByteArray(
                                    "p{0:d}".format(index).encode("utf-8")
                                )
                    parameterNamesList = [bytes(n).decode() for n in parameterNames]
                    signatureDict["parameter_names"] = parameterNamesList
                    methNamesSig = ", ".join(parameterNamesList)

                    if methNamesSig:
                        pythonSignature = "on_{0}_{1}(self, {2})".format(
                            name,
                            bytes(metaMethod.methodSignature()).decode().split("(")[0],
                            methNamesSig,
                        )
                    else:
                        pythonSignature = "on_{0}_{1}(self)".format(
                            name,
                            bytes(metaMethod.methodSignature()).decode().split("(")[0],
                        )
                    signatureDict["python_signature"] = pythonSignature

                    objectDict["methods"].append(signatureDict)

            objectsList.append(objectDict)

        _printout(json.dumps(objectsList))
        sys.exit(0)
    except (AttributeError, ImportError, xml.etree.ElementTree.ParseError) as err:
        _printerr(str(err))
        sys.exit(1)


def signatures1(formFile, projectPath):
    """
    Function to get the signatures of form elements.

    @param formFile file name of the form
    @type str
    @param projectPath directory name of the project
    @type str
    """
    sys.path.append(projectPath)
    print("mark", formFile, projectPath)

    _app = QApplication([])  # __IGNORE_WARNING__
    try:
        # 创建 QUiLoader 实例
        # loader = QUiLoader()
        loader = QtUiTools.QUiLoader()

        # 使用 QFile 打开 .ui 文件
        file = QFile(formFile)
        if not file.open(QFile.ReadOnly):
            raise IOError(f"Unable to open {formFile}")

        # 使用 loader 加载 .ui 文件
        dlg = loader.load(file)
        file.close()

        # 后续处理代码...
        print(dlg.objectName())
        sys.exit(0)

    except (AttributeError, ImportError, xml.etree.ElementTree.ParseError) as err:
        print(f"Error: {err}")
        sys.exit(1)


if __name__ == "__main__":

    if len(sys.argv) != 4:
        _printerr("Wrong number of arguments.")
        sys.exit(1)

    if sys.argv[1] == "object_name":
        objectName(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == "class_name":
        className(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == "signatures":
        signatures(sys.argv[2], sys.argv[3])
    else:
        _printerr("Unknown operation given.")
        sys.exit(1)
