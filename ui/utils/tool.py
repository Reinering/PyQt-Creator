#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author: Reiner New
email: nbxlc@hotmail.com
"""


import sys
import os




def resource_path(relative_path):
    """获取资源文件的绝对路径，适用于打包和未打包的情况"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


def startCMD(pyInterpreter):
    (pypath, pyfilename) = os.path.split(pyInterpreter)

    pythonPath = []
    pythonPath.append(pyInterpreter)
    pythonPath.append(pypath)
    pythonPath.append(os.path.join(pypath, "scripts"))
    pythonPath.append(os.path.join(pypath, "DLLs"))
    pythonPath.append(os.path.join(pypath, "Lib"))
    pythonPath.append(os.path.join(pypath, "Lib", "site-packages"))
    pythonPath.append(os.path.join(pypath, "Lib", "site-packages", "win32"))
    pythonPath.append(os.path.join(pypath, "Lib", "site-packages", "win32", "lib"))
    pythonPath.append(os.path.join(pypath, "Lib", "site-packages", "Pythonwin"))
    os.environ["PYTHONPATH"] = (';').join(pythonPath)

    os.system(f' start cmd.exe /K cd /d {pypath}')