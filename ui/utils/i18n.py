#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author: Reiner New
email: nbxlc@hotmail.com
"""
import os.path

from PySide6.QtCore import QTranslator, QLocale, QLibraryInfo, QObject, Signal
from PySide6.QtWidgets import QApplication
from manage import ROOT_PATH, UI_CONFIG

current_translator = None
qt_translator = None   # 可选：Qt 内置翻译

def init_translators():
    """程序启动时调用一次，加载 Qt 内置翻译"""
    global qt_translator
    app = QApplication.instance()
    if not qt_translator:
        qt_translator = QTranslator()
        qt_path = QLibraryInfo.path(QLibraryInfo.LibraryPath.TranslationsPath)
        if qt_translator.load(QLocale.system(), "qtbase", "_", qt_path):
            app.installTranslator(qt_translator)

def switch_language(locale_name: str = "zh_CN"):
    global current_translator
    app = QApplication.instance()

    if current_translator:
        app.removeTranslator(current_translator)

    file_path = os.path.join(ROOT_PATH, UI_CONFIG["localesPath"], f"{locale_name}.qm")

    new_translator = QTranslator()
    if new_translator.load(file_path):
        app.installTranslator(new_translator)
        current_translator = new_translator
        print(f"语言已切换为: {locale_name}")

        app.installTranslator(new_translator)

        # 核心逻辑：遍历当前程序中所有已经创建的窗口和控件
        for widget in QApplication.allWidgets():
            # 检查这个 widget 是否有 retranslateUi 方法
            # 1. 检查 self.ui.retranslateUi (Qt Designer 常用)
            if hasattr(widget, "ui") and hasattr(widget.ui, "retranslateUi"):
                widget.ui.retranslateUi(widget)
            # 2. 检查 widget 自身是否有 retranslateUi (手动编写或继承时)
            elif hasattr(widget, "retranslateUi"):
                widget.retranslateUi(widget)
    else:
        print(f"加载语言 {locale_name} 失败")

