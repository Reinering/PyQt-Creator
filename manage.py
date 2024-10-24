#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author: Reiner New
email: nbxlhc@hotmail.com
"""

import os
import sys
import platform

# 软件版本信息
APPNAME = "PyQt Creator"
VERSION = "v0.1.00"
PackageTime = ""
RUNTIMEENV = None

# 0: CRITICAL, 1: ERROR, 2: WARNING, 3: INFO, 4: DEBUG
LOGLEVEL = 4

LOGFILE = "logs/app.log"

os_platform = platform.system()
maxbit = sys.maxsize
if maxbit > 2 * 32:
    Computer_Digits = 'x64'
else:
    Computer_Digits = 'x86'

ROOT_PATH = os.getcwd()

EncodingFormat = 'gbk'

SettingPath = "./data"
SettingFile = "setting.json"

UI_CONFIG = {
    "theme": "Light",

    "startLogo": "resource/images/logo.png",
    "logoPath": f':/logo/images/logo.png',
    "iconPath": f":/images/icons",
    "gifPath": f":/images/gifs",
    "stylesheetPath": ":/qss/stylesheets",

    "Material": {
        "AcrylicBlurRadius": 15
    },
    "Update": {
        "CheckUpdateAtStartUp": True
    },
    "Folders": {
        "Download": "",
        "LocalMusic": []
    },
    "MainWindow": {
        "DpiScale": "Auto",
        "Language": "Auto"
    },
    "QFluentWidgets": {
        "ThemeColor": "#ff009faa",
        "ThemeMode": "Dark"
    }
}

# if getattr(sys, 'frozen', False):
#     BUNDLE_DIR = sys._MEIPASS
#     RUNTIMEENV = "bundle"
#     UI_CONFIG["startLogo"] = os.path.join(BUNDLE_DIR, UI_CONFIG["startLogo"])
#
#     LIBSPATH = os.path.join(BUNDLE_DIR, "libs")
# else:

BUNDLE_DIR = os.path.dirname(os.path.abspath(__file__))

LIBSPATH = os.path.join("libs")

PAGEWidgets = {
    "main": '',
    "home": '',
    "project": '',
    "designer": '',
    "pack": '',
    "other": '',
    "settings": '',
}

LIBS = {
    "pyinstaller": os.path.join(LIBSPATH, "pyinstaller"),
    "nuitka": os.path.join(LIBSPATH, "nuitka"),
    "pyenv": os.path.join("libs", "pyenv-win"),
}

IMAGE_TYPES = ['.png', '.jpg', '.jpeg', '.bmp', '.gif', '.ico', '.svg']

MIRRORS = {
    "pyenv": {
        "origin": "https://www.python.org/ftp/python",
        # "taobao": "https://npm.taobao.org/mirrors/python",
        "huawei": "https://repo.huaweicloud.com/python/",
    },
    "pip": {
        "origin": "https://pypi.org/simple/",
        "tsinghua": "https://pypi.tuna.tsinghua.edu.cn/simple/",
        "aliyun": "https://mirrors.aliyun.com/pypi/simple/",
        "tencent": "https://mirrors.cloud.tencent.com/pypi/simple/",
        "huawei": "https://mirrors.huaweicloud.com/repository/pypi/simple/",
        "douban": "https://pypi.douban.com/simple/",
    },
}

REQUIREMENTS_URLS = {
   "qfluentwidgets": {
       "pyqt5": "PyQt-Fluent-Widgets[full]",
       "pyqt6": "PyQt6-Fluent-Widgets[full]",
       "pyside6": "PySide6-Fluent-Widgets[full]"
   },
    "qfluentexpand": "https://github.com/Reinering/qfluentexpand.git"
}


SETTINGS = {
    "project": {
        "python_env_modes": ["独立模式", "跟随全局"],
        "project_types": ["PySide6", "PyQt6", "PyQt5", "PySide2"]
    },
    "designer": {
        "python_env_modes": ["独立模式", "跟随项目", "跟随全局"],
    },
    "pack": {
        "python_env_modes": ["独立模式", "跟随项目", "跟随全局"],       # ['project', 'global', 'standalone']
        "pyinstaller": {},
        "nuitka": {},
        "setup": {
            "filepath": ""
        },
    },
    "other": {
        "python_env_modes": ["独立模式", "跟随项目", "跟随全局"],
        "project_types": ["PySide6", "PyQt6", "PyQt5", "PySide2"]
    },
    "settings": {
        "theme": ['Light', 'Dark'],
        "language": ['Auto', 'zh_CN', 'en_US'],
        "dpi": ['Auto', '96', '120', '144', '192'],
        "update": ['CheckUpdateAtStartUp', 'CheckUpdateAtEnd'],
        "python_env_modes": ["现有环境", "Pyenv 环境"],           # ["system", "venv", "pyenv", "conda"]
        "pyenv_maxbit": ['x64', 'x86'],
    }
}


CURRENT_SETTINGS = {
    "project": {
        "mode": "独立模式",
        "custom_python_path": "",
        "project_path": "",
        "project_name": "",
        "project_type": 'PySide6',
        "recently_opened": []
    },
    "designer": {
        "mode": "独立模式",
        "custom_python_path": "",
        "fileUI": ''
    },
    "pack": {
        "mode": "独立模式",
        "custom_python_path": "",
        "main": "",
        "outPath": "",
        "outName": "",
        "pyinstaller": {},
        "nuitka": {},
        "setup": {
            "filepath": ""
        },
    },
    "other": {
        "mode": "独立模式",
        "custom_python_path": "",
        "project_type": 'PySide6'
    },
    "settings": {
        "theme": 'Light',
        "language": 'Auto',
        "dpi": 'Auto',
        "update": 'CheckUpdateAtStartUp',
        "mode": "Pyenv 环境",
        "custom_python_path": "",
        "pyenv_path": LIBS["pyenv"],
        "pyenv_current_version": "",
        "pyenv_mirror_url": "origin",
        "pip_mirror_url": "origin",
        "editors": ["notepad"],
        "editor": "notepad",
    }
}