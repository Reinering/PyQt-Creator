#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author: Reiner
email: nbxlc@hotmail.com
"""

# from __future__ import print_function
import ctypes
import sys
import getopt
import logging.handlers
import os
import platform
import time
import simplejson as json
import socket  # Windows 系统
if os.name == "posix":
    import fcntl  # Unix 系统

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QSplashScreen, QMessageBox
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication

import qfluentwidgets

from manage import (
    UI_CONFIG, LOGLEVEL, LOGFILE, PIDFILE, ROOT_PATH,
    SettingPath, SettingFile, CURRENT_SETTINGS,
    RUNTIMEENV, BUNDLE_DIR
)
from ui.MainWindow import MainWindow
from common.pyinstaller import PyinstallerPackage
from common.nuitka import NuitkaPackage
from common.pipreqs import Pipreqs
from common.config import diff_config
from common.utils import is_admin


# from pycrunch_trace.client.api import trace


def log(LOGLEVEL):
    levels = [logging.CRITICAL, logging.ERROR, logging.WARNING, logging.INFO, logging.DEBUG]
    if not os.path.exists("./logs"):
        os.mkdir("logs")
    LOG_FILE = LOGFILE
    logger = logging.getLogger("myapp")
    hdlr = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=1024*10240, backupCount=400, encoding='utf-8')     # 按大小进行分割
    # hdlr = logging.handlers.TimedRotatingFileHandler(LOG_FILE, when='D', interval=1, backupCount=40)  # 按时间进行分割
    logging.basicConfig(level=levels[LOGLEVEL],
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        filename=LOG_FILE,
                        filemode='a+')
    logger.addHandler(hdlr)
    logger.setLevel(LOGLEVEL)

class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

def suppress_keyboard_interrupt_message():
    old_excepthook = sys.excepthook

    def new_hook(exctype, value, traceback):
        if exctype != KeyboardInterrupt:
            old_excepthook(exctype, value, traceback)
        else:
            print('\nKeyboardInterrupt ...')
            print('do something after Interrupt ...')

    sys.excepthook = new_hook

def create_file(fullPath):
    """
    创建日志文件夹和日志文件
    :param filename:
    :return:
    """
    (filepath, filename) = os.path.split(fullPath)
    if not os.path.isdir(filepath):  # 无文件夹时创建
        os.makedirs(filepath)
    if not os.path.isfile(fullPath):  # 无文件时创建
        fd = open(fullPath, mode="w", encoding="utf-8")
        fd.close()

def readConfig():
    if not os.path.exists(os.path.join(ROOT_PATH, SettingPath)):
        os.mkdir(SettingPath)

    if not os.path.exists(os.path.join(ROOT_PATH, SettingPath, SettingFile)):
        with open(os.path.join(ROOT_PATH, SettingPath, SettingFile), "w") as f:
            json.dump(CURRENT_SETTINGS, f, indent=4)
            f.flush()
            f.close()
    else:
        with open(os.path.join(ROOT_PATH, SettingPath, SettingFile), "r") as f:
            data = json.load(f)
            diff_config(data, CURRENT_SETTINGS)

    if not os.path.exists(os.path.join(ROOT_PATH, SettingPath, "pyinstaller.json")):
        with open(os.path.join(ROOT_PATH, SettingPath, "pyinstaller.json"), "w") as f:
            json.dump(PyinstallerPackage.PYINSTALLER_PARAMS, f, indent=4)

    if not os.path.exists(os.path.join(ROOT_PATH, SettingPath, "nuitka.json")):
        with open(os.path.join(ROOT_PATH, SettingPath, "nuitka.json"), "w") as f:
            json.dump(NuitkaPackage.NUITKA_PARAMS, f, indent=4)

    if not os.path.exists(os.path.join(ROOT_PATH, SettingPath, "pipreqs.json")):
        with open(os.path.join(ROOT_PATH, SettingPath, "pipreqs.json"), "w") as f:
            json.dump(Pipreqs.PIPREQS_PARAMS, f, indent=4)


def setTheme():
    if CURRENT_SETTINGS["settings"]["theme"] == "Dark":
        theme = qfluentwidgets.Theme.DARK
    elif CURRENT_SETTINGS["settings"]["theme"] == "Light":
        theme = qfluentwidgets.Theme.LIGHT
    qfluentwidgets.setTheme(theme)


def acquire_lock():
    lock_file = PIDFILE
    if os.name == "posix":  # Unix 系统
        fp = open(PIDFILE, "w")
        try:
            fcntl.flock(fp.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            return fp
        except IOError:
            print("另一个 EXE 或脚本实例正在运行")
            sys.exit(1)
    elif os.name == "nt":  # Windows 系统
        try:
            if os.path.exists(lock_file):
                os.unlink(lock_file)
            fp = open(lock_file, "w")
            fp.write(str(os.getpid()))
            return fp
        except OSError:
            print("另一个 EXE 或脚本实例正在运行")
            sys.exit(1)


# @trace()
def main(argv=None):

    if argv is None:
        argv = sys.argv

    try:
        try:
            lock = acquire_lock()

            # opts, args = getopt.getopt(argv[1:], "h", ["help"])
            log(LOGLEVEL)
            app = QApplication(sys.argv)
            app.setAttribute(Qt.ApplicationAttribute.AA_DontCreateNativeWidgetSiblings)

            # 没有运行配置时，复制默认配置
            try:
                readConfig()
            except Exception as e:
                QMessageBox.critical(None, "Error", "Read Config Error!")
                raise Exception("Read Config Error!", e)

            # 设置theme
            setTheme()

            # log enable
            log(LOGLEVEL)

            # internationalization i18n setting
            # fluentTranslator = FluentTranslator(UI_CONFIG["MainWindow"]["Language"])
            # translator = QTranslator()
            # translator.load(UI_CONFIG["MainWindow"]["Language"], "gallery", ".", ":/gallery/i18n")
            #
            # app.installTranslator(fluentTranslator)
            # app.installTranslator(translator)

            # 启动图标
            existPic = os.path.exists(os.path.join(BUNDLE_DIR, UI_CONFIG["startLogo"]))
            if existPic:
                splash = QSplashScreen(QPixmap(os.path.join(BUNDLE_DIR, UI_CONFIG["startLogo"])))
                splash.show()
                time.sleep(2)       # 启动图标显示2s

            ui = MainWindow()
            ui.show()
            if existPic:
                splash.finish(ui)

            if '--hidden' in sys.argv:
                ui.hide()

            lock.close()
            sys.exit(app.exec())
        except getopt.error as msg:
            raise Usage(msg)
    except Usage as err:
        print >> sys.stderr, err.msg
        print >> sys.stderr, "for help use --help"
        return 2



if __name__ == "__main__":
    # 捕获全局的 KeyboardInterrupt 异常
    suppress_keyboard_interrupt_message()

    # 判断程序运行环境: pyinstaller or pycharm
    if RUNTIMEENV == "bundle":
        # running in a bundle
        # # 强制以管理员权限运行
        if is_admin():
            # 将要运行的代码加到这里
            sys.exit(main())
        else:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
    else:
        # running live
        sys.exit(main())

        # if is_admin():
        #     # 将要运行的代码加到这里
        #     sys.exit(main())
        # else:
        #     ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
