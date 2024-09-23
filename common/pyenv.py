#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author: Reiner New
email: nbxlc@hotmail.com
"""


import os
import subprocess


class PyEnv():
    def __init__(self):
        self.pyenvPath = os.path.join('', 'pyenv-win/bin/pyenv')

    def getPyVers(self):

        result = subprocess.run([self.pyenvPath, 'install', '--list'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"")
        else:
            print(f"Error: {result.stderr}")




class PyVenvManager():
    """
    Python virtual environment manager
    """

    def __init__(self, pyenv_root_path):
        self.venvPath = os.path.join(pyenv_root_path, 'bin\\pyenv.bat')

        self.setEnviron(PYTHON_BUILD_MIRROR_URL="https://npm.taobao.org/mirrors/python")

    def setEnviron(self, **kwargs):
        for key, value in kwargs.items():
            os.environ[key] = value

    def cmd(self, cmd):

        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            # print(f"{result.stdout}")
            return (True, f"{result.stdout}")
        else:
            print(f"Error: {result.stderr}")
            return (False, f"Error: {result.stderr}")

    def list(self):
        command = [self.venvPath, 'install', '--list']
        return self.cmd(command)

    def install(self, version):
        command = [self.venvPath, 'install', version]
        return self.cmd(command)

    def update(self):
        command = [self.venvPath, 'update']
        return self.cmd(command)

    def versions(self):
        command = [self.venvPath, 'versions']
        return self.cmd(command)

    def shell(self, version):
        command = [self.venvPath, 'shell', version]
        return self.cmd(command)

    def global_(self, version):
        command = [self.venvPath, 'global', version]
        return self.cmd(command)

    def lcoal_(self, version):
        command = [self.venvPath, 'local', version]
        return self.cmd(command)

    def uninstall(self, version):
        command = [self.venvPath, 'uninstall', version]
        return self.cmd(command)

    def help(self):
        command = [self.venvPath, 'help']
        return self.cmd(command)

    def create_venv(self, env_name):
        pass

    def activate_venv(self, path):
        pass

    def install_package(self, package_name):
        pass