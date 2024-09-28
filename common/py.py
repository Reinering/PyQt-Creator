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

# from pathlib import Path
# pyinstaller_path = Path(sys.executable).parent.joinpath('Scripts\pyinstaller.exe')


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

    QFLUENTEXPAND = "Lib\\site-packages\\qfluentexpand"
    DESIGNER_PYSIDE6 = os.path.join(QFLUENTEXPAND, "tools\\pyside6-designer.py")
    PYSIDE6_PLUGINS = os.path.join(QFLUENTEXPAND, "plugins")

    # pyinstaller
    PYINSTALLER = os.path.join(SCRIPTS, "pyinstaller.exe")

    # nuitka
    NUITKA = os.path.join(SCRIPTS, "nuitka.bat")

    # pipreqs
    PIPREQS = os.path.join(SCRIPTS, "pipreqs.exe")

    def path(self, interpreterPath=None):
        if interpreterPath:
            (interpreterFolder, name) = os.path.split(interpreterPath)
            return os.path.join(interpreterFolder, self.value)
        else:
            return self.value


class PyInterpreter:

    def setInterpreter(self, path):
        self.interpreterPath = path
        (self.interpreterFolder, name) = os.path.split(path)

    def setEnviron(self, **kwargs):
        for key, value in kwargs.items():
            os.environ[key] = value

    def cmd(self, cmd):
        print(f"cmd: {cmd}")
        logging.debug(f"cmd: {cmd}")

        result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
        if result.returncode == 0:
            print(f"{result.stdout}")
            logging.debug(f"{result.stdout}")
            return (True, f"{result.stdout}")
        else:
            print(f"Error: {result.stderr}")
            logging.debug(f"Error: {result.stderr}")
            return (False, f"Error: {result.stderr}")

    def popen(self, cmd):
        print(f"cmd: {cmd}")

        result = subprocess.run(cmd, capture_output=True, shell=True)
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

    def py_popen(self, cmd):
        command = list(cmd)
        command.insert(0, self.interpreterPath)
        return self.cmd(command)

    def version(self):
        return self.cmd([self.interpreterPath, '--version'])


