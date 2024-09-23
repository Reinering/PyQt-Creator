#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author: Reiner
email: nbxlc@hotmail.com
"""


import win32api
import win32con
from manage import Computer_Digits



# 查找的软件名称
def findProgramPath(name):
    path = None
    key = rf'SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\{name}'

    try:
        #通过获取Windows注册表查找软件
        if Computer_Digits == 'x64':
            key = win32api.RegOpenKey(win32con.HKEY_LOCAL_MACHINE, key, 0, win32con.KEY_READ | win32con.KEY_WOW64_64KEY)
        else:
            key = win32api.RegOpenKey(win32con.HKEY_LOCAL_MACHINE, key, 0, win32con.KEY_READ)
            # key = win32api.RegOpenKeyEx(win32con.HKEY_LOCAL_MACHINE, "SOFTWARE\\Microsoft", 0, win32con.KEY_WOW64_64KEY | win32con.KEY_READ, &hKey)

        info2 = win32api.RegQueryInfoKey(key)
        for j in range(0, info2[1]):
            key_value = win32api.RegEnumValue(key, j)[1]
            if key_value.upper().endswith(name.upper()):
                path = key_value
                break

        win32api.RegCloseKey(key)
    except Exception as e:
        print(e)
        
    return path

# 下面可忽略
# sys.path.append(findProgramPath())#将获取的安装路径添加到环境变量


if __name__ == "__main__":

    print(findProgramPath("wireshark"))