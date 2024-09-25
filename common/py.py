#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author: Reiner New
email: nbxlc@hotmail.com
"""

from enum import Enum
import sys
import os
import subprocess
import requests
import logging



def getPyVer():
    # 获取Python版本列表
    response = requests.get('https://api.github.com/repos/python/cpython/tags')

    # 解析JSON数据
    data = response.json()

    # 获取Python版本列表
    python_versions = [tag['name'] for tag in data if tag['name'].startswith('v')]

    # 打印Python版本列表
    return python_versions



class PyPath(Enum):

    SCRIPTS = "scripts"

    # pyqt5
    PYQT5 = "Lib\\site-packages\\PyQt5"
    PYQT5_DESIGNER = os.path.join(PYQT5, "designer.exe")
    PYQT5_UIC = os.path.join(PYQT5, SCRIPTS, "pyuic6.exe")
    PYQT5_RCC = os.path.join(PYQT5, SCRIPTS, "pyrcc5.exe")

    # pyqt6
    PYQT6 = "Lib\\site-packages\\PyQt6"
    PYQT6_DESIGNER = os.path.join(PYQT6, "designer.exe")
    PYQT6_UIC = os.path.join(PYQT6, SCRIPTS, "pyuic6.exe")
    PYQT6_RCC = os.path.join(PYQT6, SCRIPTS, "pyrcc6.exe")

    # pyside6
    PYSIDE6 = "Lib\\site-packages\\PySide6"
    PYSIDE6_DESIGNER = os.path.join(PYSIDE6, "designer.exe")
    PYSIDE6_UIC = os.path.join(PYSIDE6, SCRIPTS, "pyside6-uic.exe")
    PYSIDE6_RCC = os.path.join(PYSIDE6, SCRIPTS, "pyside6-rcc.exe")

    # pyinstaller
    PYINSTALLER = os.path.join(SCRIPTS, "pyinstaller.exe")

    # nuitka
    NUITKA = os.path.join(SCRIPTS, "nuitka.bat")


    def path(self, interpreterPath):
        return os.path.join(interpreterPath, self.value)


class PyInterpreter:

    def setInterpreter(self, path):
        self.interpreterPath = path
        (self.interpreterFolder, name) = os.path.split(path)

    def cmd(self, cmd):
        print(f"cmd: {cmd}")

        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"{result.stdout}")
            logging.debug(f"{result.stdout}")
            return (True, f"{result.stdout}")
        else:
            print(f"Error: {result.stderr}")
            logging.debug(f"Error: {result.stderr}")
            return (False, f"Error: {result.stderr}")

    def pip(self, *args):
        command = [self.interpreterPath, '-m', 'pip']
        command.extend(args)
        return self.cmd(command)

    def py(self, cmd):
        command = [self.interpreterPath, cmd]
        return self.cmd(command)



