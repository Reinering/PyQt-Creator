#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author: Reiner New
email: nbxlc@hotmail.com
"""


import os
import sys
import platform


os_platform = platform.system()


# macos的自动启动未实现

def getAutoLaunch(app_name):
    if os_platform == "Windows":
        from .reg import get_reg_value
        auto_launch, _ = get_reg_value(
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            app_name,
            scope='user'
        )
        return auto_launch
    elif os_platform == "Linux":
        autostart_path = os.path.expanduser("~/.config/autostart")
        desktop_file = os.path.join(autostart_path, f"{app_name}.desktop")
        return os.path.exists(desktop_file)
    elif os_platform == "Darwin":
        from common.macos_launch import is_login_item
        return is_login_item(app_name)
    else:
        return False

def setAutoLaunch(app_name, app_path, enable=True, isHidden=False):
    if os_platform == "Windows":
        from .reg import set_reg_value, delete_reg_value
        if enable:
            if isHidden:
                app_path = f'"{app_path}" --hidden'

            set_reg_value(
                r"Software\Microsoft\Windows\CurrentVersion\Run",
                app_name,
                app_path,
                scope='user'
            )
        else:
            delete_reg_value(
                r"Software\Microsoft\Windows\CurrentVersion\Run",
                app_name,
                scope='user'
            )
    elif os_platform == "Linux":
        autostart_path = os.path.expanduser("~/.config/autostart")
        desktop_file = os.path.join(autostart_path, f"{app_name}.desktop")
        if enable:
            if not os.path.exists(autostart_path):
                os.makedirs(autostart_path)
            with open(desktop_file, 'w') as f:
                f.write(f"[Desktop Entry]\nType=Application\nExec={app_path}\nHidden=false\nNoDisplay=false\nX-GNOME-Autostart-enabled=true\nName={app_name}\n")
        else:
            if os.path.exists(desktop_file):
                os.remove(desktop_file)
    elif os_platform == "Darwin":
        from common.macos_launch import add_login_item, remove_login_item
        if enable:
            add_login_item(app_name, app_path)
        else:
            remove_login_item(app_name)

def create_startup_shortcut(app_name, app_path):
    import shutil

    startup_folder = os.path.join(os.environ['APPDATA'], 'Microsoft\\Windows\\Start Menu\\Programs\\Startup')
    shortcut_path = os.path.join(startup_folder, app_name + '.lnk')

    # 将自身的可执行文件复制到启动文件夹
    shutil.copy2(app_path, shortcut_path)