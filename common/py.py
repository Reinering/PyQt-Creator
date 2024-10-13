#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author: Reiner New
email: nbxlc@hotmail.com
"""

from enum import Enum
import os
import signal
import psutil
import subprocess
import requests



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
    PYQT5_UIC = os.path.join(SCRIPTS, "pyuic6.exe")
    PYQT5_RCC = os.path.join(SCRIPTS, "pyrcc5.exe")

    # pyqt6
    PYQT6 = "Lib\\site-packages\\PyQt6"
    PYQT6_DESIGNER = os.path.join(PYQT6, "designer.exe")
    PYQT6_UIC = os.path.join(SCRIPTS, "pyuic6.exe")
    PYQT6_RCC = os.path.join(SCRIPTS, "pyrcc6.exe")

    # pyside6
    PYSIDE6 = "Lib\\site-packages\\PySide6"
    PYSIDE6_DESIGNER = os.path.join(PYSIDE6, "designer.exe")
    PYSIDE6_UIC = os.path.join(SCRIPTS, "pyside6-uic.exe")
    PYSIDE6_RCC = os.path.join(SCRIPTS, "pyside6-rcc.exe")

    QFLUENTEXPAND = "Lib\\site-packages\\qfluentexpand"
    DESIGNER_PYSIDE6 = os.path.join(QFLUENTEXPAND, "tools\\designer.py")
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

    def __init__(self):
        self.process = None

    def setInterpreter(self, path):
        self.interpreterPath = path
        (self.interpreterFolder, name) = os.path.split(path)

    def setEnviron(self, **kwargs):
        for key, value in kwargs.items():
            os.environ[key] = value

    def stop(self):
        if self.process and not isinstance(self.process, subprocess.CompletedProcess):
            parent = psutil.Process(self.process.pid)
            children = parent.children(recursive=True)
            # print("pid", parent, children)
            for child in children:
                child.kill()
            self.process.kill()
            # self.process.terminate()

            # try:
            #     pid = self.process.pid
            #     cmd = "taskkill /pid {} -t -f".format(str(pid))
            #     pp = subprocess.Popen(args=cmd,
            #                           stdin=subprocess.PIPE,
            #                           stdout=subprocess.PIPE,
            #                           stderr=subprocess.PIPE,
            #                           shell=True)
            #     out = str(pp.stdout.read(), encoding="utf-8")
            # except Exception as e:
            #     print(e)

            self.process = None

    def cmd(self, cmd):
        print(f"cmd: {cmd}")

        self.process = subprocess.run(cmd, capture_output=True, text=True, shell=True)
        if self.process.returncode == 0:
            print(f"{self.process.stdout}")
            return [True, f"{self.process.stdout}"]
        else:
            print(f"Error: {self.process.stderr}")
            return (False, f"Error: {self.process.stderr}")

    def popen(self, cmd):
        print(f"cmd: {cmd}")

        # self.process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        # stdout, stderr = self.process.communicate()
        # print(f"{stdout.decode('gbk'), stderr.decode('gbk')}")
        # if self.process.returncode == 0:
        #     return [True, f"{stdout.decode('gbk')}"]
        # else:
        #     return (False, f"Error: {stderr.decode('gbk')}", f"Log: {stdout.decode('gbk')}")

        env = os.environ.copy()

        self.process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        outs = []
        try:
            while True:
                line = self.process.stdout.readline().decode('gbk').strip('\n')\
                    .strip('\r').strip(' ').replace('\\\\', '\\').replace('\\\\', '\\')
                if line == '' and self.process.poll() != None:
                    break
                elif line == '\n' or line == '\r' or line == '\r\n' or line == ' ' or line == '':
                    continue
                print(line)
                outs.append(line)
        except Exception as e:
            print(e)
            return (False, f"Error: {e}")

        if "nuitka" in cmd:
            if len(outs) > 50:
                outs = outs[-50:]

        # out = '\n'.join(outs)
        if self.process.returncode == 0:
            return [True, f"{outs}"]
        else:
            return (False, f"Error: {outs}")

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


