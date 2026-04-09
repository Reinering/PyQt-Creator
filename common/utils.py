#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author: Reiner New
email: nbxlc@hotmail.com
"""

import ctypes

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False



from pathlib import Path


def get_all_source_files(root_dir: str = "."):
    """返回当前目录（含子目录）下所有 .py 和 .ui 文件的完整路径列表"""
    files = []

    # 方法1：使用 pathlib（Python 3.6+ 推荐，更现代）
    root = Path(root_dir)
    for ext in ["*.py", "*.ui"]:
        files.extend(root.rglob(ext))

    # 方法2：使用 os.walk（兼容性更好）
    # for root, dirs, filenames in os.walk(root_dir):
    #     for filename in filenames:
    #         if filename.endswith(('.py', '.ui')):
    #             files.append(os.path.join(root, filename))

    # 转为普通字符串路径，并排序（方便查看）
    file_list = sorted([str(f) for f in files])

    return file_list
