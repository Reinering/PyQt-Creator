#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author: Reiner New
email: nbxlc@hotmail.com
"""


import os
import subprocess



class PyVenvManager():
    """
    Python virtual environment manager
    """

    def __init__(self, pyenv_root_path):
        self.venvPath = os.path.join(pyenv_root_path, 'bin\\pyenv.bat')
        self.process = None

    def setEnviron(self, **kwargs):
        for key, value in kwargs.items():
            os.environ[key] = value

    def stop(self):
        if self.process:
            self.process.terminate()
            self.process = None

    def cmd(self, cmd):
        print(f"cmd: {cmd}")

        self.process = subprocess.run(cmd, capture_output=True, text=True, shell=True)
        if self.process.returncode == 0:
            return (True, f"{self.process.stdout}")
        else:
            return (False, f"Error: {self.process.stderr}")

    def list(self):
        command = [self.venvPath, 'install', '--list']
        return self.cmd(command)

    def install(self, version):
        if not version:
            return (False, "Error: version is empty")
        command = [self.venvPath, 'install', version]
        return self.cmd(command)

    def uninstall(self, version):
        if not version:
            return (False, "Error: version is empty")
        command = [self.venvPath, 'uninstall', version]
        return self.cmd(command)

    def update(self):
        command = [self.venvPath, 'update']
        return self.cmd(command)

    def versions(self):
        command = [self.venvPath, 'versions']
        return self.cmd(command)

    def rehash(self):
        command = [self.venvPath, 'rehash']
        return self.cmd(command)

    def shell(self, version):
        if not version:
            return (False, "Error: version is empty")
        command = [self.venvPath, 'shell', version]
        return self.cmd(command)

    def global_(self, version):
        if not version:
            return (False, "Error: version is empty")
        command = [self.venvPath, 'global', version]
        return self.cmd(command)

    def lcoal_(self, version):
        if not version:
            return (False, "Error: version is empty")
        command = [self.venvPath, 'local', version]
        return self.cmd(command)

    def help(self):
        command = [self.venvPath, 'help']
        return self.cmd(command)

    def install_package(self, package_name):
        pass