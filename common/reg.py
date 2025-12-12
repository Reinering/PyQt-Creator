#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author: Reiner New
email: nbxlc@hotmail.com
"""


import os
if os.name != "posix":
    import winreg


def check_path_in_path(check_path, scope='user'):
    """
    检查路径是否在 PATH 环境变量中
    :param check_path: 要检查的路径
    :param scope: 'user' 表示用户环境变量，'system' 表示系统环境变量
    :return: 如果路径存在返回 True，否则返回 False
    """
    if scope == 'user':
        key_path = r"Environment"
        reg_hive = winreg.HKEY_CURRENT_USER
    elif scope == 'system':
        key_path = r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment"
        reg_hive = winreg.HKEY_LOCAL_MACHINE
    else:
        raise ValueError("scope 参数必须为 'user' 或 'system'")

    try:
        # 打开注册表键
        key = winreg.OpenKey(reg_hive, key_path, 0, winreg.KEY_READ)
        # 读取当前 PATH
        current_path, _ = winreg.QueryValueEx(key, 'Path')
        # 关闭注册表键
        winreg.CloseKey(key)
        # 检查路径是否存在
        return check_path in current_path.split(';')
    except WindowsError as e:
        print(f"读取 PATH 失败: {e}")
        return False

def check_env_variable(var_name, scope='user'):
    """
    检查环境变量是否存在
    :param var_name: 环境变量名称
    :param scope: 'user' 表示用户环境变量，'system' 表示系统环境变量
    :return: 如果变量存在返回 True，否则返回 False
    """
    if scope == 'user':
        key_path = r"Environment"
        reg_hive = winreg.HKEY_CURRENT_USER
    elif scope == 'system':
        key_path = r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment"
        reg_hive = winreg.HKEY_LOCAL_MACHINE
    else:
        raise ValueError("scope 参数必须为 'user' 或 'system'")

    try:
        # 打开注册表键
        key = winreg.OpenKey(reg_hive, key_path, 0, winreg.KEY_READ)
        # 尝试读取环境变量
        winreg.QueryValueEx(key, var_name)
        # 关闭注册表键
        winreg.CloseKey(key)
        return True
    except WindowsError:
        return False


def append_to_path(new_path, scope='user'):
    """
    将路径追加到 PATH 环境变量
    :param new_path: 要添加的路径
    :param scope: 'user' 表示用户环境变量，'system' 表示系统环境变量
    """
    if scope == 'user':
        key_path = r"Environment"
        reg_hive = winreg.HKEY_CURRENT_USER
    elif scope == 'system':
        key_path = r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment"
        reg_hive = winreg.HKEY_LOCAL_MACHINE
    else:
        raise ValueError("scope 参数必须为 'user' 或 'system'")

    try:
        # 打开注册表键
        key = winreg.OpenKey(reg_hive, key_path, 0, winreg.KEY_ALL_ACCESS)
        # 读取当前 PATH
        current_path, _ = winreg.QueryValueEx(key, 'Path')
        # 确保路径不重复
        if new_path not in current_path:
            new_path_value = f"{current_path};{new_path}" if current_path else new_path
            # 设置新的 PATH
            winreg.SetValueEx(key, 'Path', 0, winreg.REG_EXPAND_SZ, new_path_value)
            print(f"已将 {new_path} 添加到 PATH")
        else:
            print(f"{new_path} 已在 PATH 中")
        # 关闭注册表键
        winreg.CloseKey(key)
    except WindowsError as e:
        print(f"设置 PATH 失败: {e}")

def set_environment_variable(var_name, var_value, scope='user'):
    """
    设置 Windows 环境变量
    :param var_name: 环境变量名称
    :param var_value: 环境变量值
    :param scope: 'user' 表示用户环境变量，'system' 表示系统环境变量
    """
    # 根据 scope 选择注册表路径
    if scope == 'user':
        key_path = r"Environment"
        reg_hive = winreg.HKEY_CURRENT_USER
    elif scope == 'system':
        key_path = r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment"
        reg_hive = winreg.HKEY_LOCAL_MACHINE
    else:
        raise ValueError("scope 参数必须为 'user' 或 'system'")

    try:
        # 打开注册表键
        key = winreg.OpenKey(reg_hive, key_path, 0, winreg.KEY_SET_VALUE)
        # 设置环境变量
        winreg.SetValueEx(key, var_name, 0, winreg.REG_SZ, var_value)
        # 关闭注册表键
        winreg.CloseKey(key)
        print(f"成功设置环境变量 {var_name} = {var_value}")
    except WindowsError as e:
        print(f"设置环境变量失败: {e}")

def get_reg_value(key_path, value_name, scope='user'):
    """
    获取注册表值
    :param key_path: 注册表键路径
    :param value_name: 注册表值名称
    :param scope: 'user' 表示用户注册表，'system' 表示系统注册表
    :return: 注册表值，如果不存在则返回 None
    """
    if scope == 'user':
        reg_hive = winreg.HKEY_CURRENT_USER
    elif scope == 'system':
        reg_hive = winreg.HKEY_LOCAL_MACHINE
    else:
        raise ValueError("scope 参数必须为 'user' 或 'system'")

    try:
        # 打开注册表键
        key = winreg.OpenKey(reg_hive, key_path, 0, winreg.KEY_READ)
        # 读取注册表值
        value, regtype = winreg.QueryValueEx(key, value_name)
        # 关闭注册表键
        winreg.CloseKey(key)
        return value, regtype
    except WindowsError:
        return None, None

def set_reg_value(key_path, value_name, value_data, scope='user'):
    """
    设置注册表值
    :param key_path: 注册表键路径
    :param value_name: 注册表值名称
    :param value_data: 注册表值数据
    :param scope: 'user' 表示用户注册表，'system' 表示系统注册表
    """
    if scope == 'user':
        reg_hive = winreg.HKEY_CURRENT_USER
    elif scope == 'system':
        reg_hive = winreg.HKEY_LOCAL_MACHINE
    else:
        raise ValueError("scope 参数必须为 'user' 或 'system'")

    try:
        # 打开注册表键
        key = winreg.OpenKey(reg_hive, key_path, 0, winreg.KEY_SET_VALUE)
        # 设置注册表值
        winreg.SetValueEx(key, value_name, 0, winreg.REG_SZ, value_data)
        # 关闭注册表键
        winreg.CloseKey(key)
        print(f"成功设置注册表值 {value_name} = {value_data}")
    except WindowsError as e:
        print(f"设置注册表值失败: {e}")

def delete_reg_value(key_path, value_name, scope='user'):
    """
    删除注册表值
    :param key_path: 注册表键路径
    :param value_name: 注册表值名称
    :param scope: 'user' 表示用户注册表，'system' 表示系统注册表
    """
    if scope == 'user':
        reg_hive = winreg.HKEY_CURRENT_USER
    elif scope == 'system':
        reg_hive = winreg.HKEY_LOCAL_MACHINE
    else:
        raise ValueError("scope 参数必须为 'user' 或 'system'")

    try:
        # 打开注册表键
        key = winreg.OpenKey(reg_hive, key_path, 0, winreg.KEY_SET_VALUE)
        # 删除注册表值
        winreg.DeleteValue(key, value_name)
        # 关闭注册表键
        winreg.CloseKey(key)
        print(f"成功删除注册表值 {value_name}")
    except WindowsError as e:
        print(f"删除注册表值失败: {e}")


# 示例：获取注册表值
# value, regtype = get_reg_value(r"Software\MyApp", "MyValue", scope='user')
# print(f"注册表值: {value}, 类型: {regtype}")
# 示例：设置注册表值
# set_reg_value(r"Software\MyApp", "MyValue", "MyData", scope='user')
# 示例：删除注册表值
# delete_reg_value(r"Software\MyApp", "MyValue", scope='user')
# 示例：检查环境变量是否存在
# exists = check_env_variable('MY_VARIABLE', scope='user')
# print(f"环境变量存在: {exists}")
# 示例：将路径添加到 PATH 环境变量
# append_to_path(r"C:\MyApp\bin", scope='user')
# 示例：检查路径是否在 PATH 环境变量中
# exists_in_path = check_path_in_path(r"C:\MyApp\bin", scope='user')
# print(f"路径在 PATH 中: {exists_in_path}")

# 示例：设置用户环境变量
# set_environment_variable('MY_VARIABLE', 'my_value', scope='user')

# 示例：设置系统环境变量（需要管理员权限）
# set_environment_variable('MY_VARIABLE', 'my_value', scope='system')

# 示例：将某路径添加到用户 PATH
# append_to_path(r"C:\MyApp\bin", scope='user')