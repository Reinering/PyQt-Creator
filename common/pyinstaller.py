#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author: Reiner New
email: nbxlc@hotmail.com
"""

import subprocess
import datetime
import platform
import os
import sys
from pathlib import Path
import re

os_ver = platform.win32_ver()
print("操作系统：", os_ver)

# maxbit = sys.maxsize
maxbit = int(platform.architecture()[0][:-3])
print("计算机位数：", maxbit)
if maxbit >= 2 * 32:
    Computer_Digits = 'x64'
else:
    Computer_Digits = 'x86'

pyinstaller_path = Path(sys.executable).parent.joinpath('Scripts\pyinstaller.exe')

Type = {
    1: 'Alpha',
    2: 'Beta',
    3: 'RC',
    4: 'Release'
}

class Package:
    def __init__(self):
        self.projectFolder = os.getcwd()
        self.computer_digits = Computer_Digits
        self.typeNum = 2
        self.mainFile = "main.py"
        self.cacheOutPath = 'dist'

        self.now = datetime.datetime.now().strftime("%Y%m%d%H%M")


        self.packageArgs = {
            'console': True,  # [True, False] -w 关闭， -c(默认) 开启 开启或关闭显示控制台 (只对Windows有效)
            'debug': False,  # [True, False] -d [{all,imports,bootloader,noarchive} 产生debug版本的可执行文件
            'specPath': '',
            # --specpath 指定spec文件的生成目录,如果没有指定,而且当前目录是PyInstaller的根目录,会自动创建一个用于输出(spec和生成的可执行文件)的目录.如果没有指定,而当前目录不是PyInstaller的根目录,则会输出到当前的目录下.
            'importPath': '',
            # -p, -–path=DIR 设置导入路径(和使用PYTHONPATH效果相似).可以用路径分割符(Windows使用分号,Linux使用冒号)分割,指定多个目录.也可以使用多个-p参数来设置多个导入路径
            'excludeModule': '',  # –exclude-module 需要排除的module
            'hiddenImport': [],  # –hidden-import 打包额外py库
            'iconPath': '',
            # -i 指定程序图标 –icon=<FILE.ICO> 将file.ico添加为可执行文件的资源 –icon=<FILE.EXE,N> 将file.exe的第n个图标添加为可执行文件的资源  (只对Windows系统有效)
            'workpath': '',  # --workpath WORKPATH 生成过程中的中间文件存放目录，默认：当前目录的build文件夹内
            'logLevel': 'INFO',
            # --log-level LEVEL 控制编译时pyi打印的信息，一共有6个等级，由低到高分别为TRACE DEBUG INFO(默认) WARN ERROR CRITICAL。也就是默认清空下，不打印TRACE和DEBUG信息
            'outType': 'FILE',  # ['FOLDER', 'FILE'] 打包的文件类型：-F 产生一个文件用于部署；-D 产生一个目录用于部署 (默认)
            'outName': '',  # -n NAME 打包的文件名 可选的项目(产生的spec的)名字.如果省略,第一个脚本的主文件名将作为spec的名字
            'distpath': '',  # --distpath DIR 生成文件存放目录，当前目录的dist文件夹内
            'addData': [],  # -add-data <SRC;DEST or SRC:DEST> 打包额外资源
            'addBinary': [],  # --add-binary <SRC;DEST or SRC:DEST> 打包额外的代码
            'isClean': False,  # [True, False] --clean 在本次编译开始时，清空上一次编译生成的各种文件,默认：不清除
            'encode': '',  # -a, --ascii 不包含unicode支持,默认：尽可能支持unicode
            'isCover': False,  # [True, False] -y, --noconfirm 如果dist文件夹内已经存在生成文件，则不询问用户，直接覆盖, 默认：询问是否覆盖
            'upxDir': '',  # --upx-dir UPX_DIR UPX实用程序的路径（默认值：搜索执行路径）
            'versionFile': '',  # --version-file FILE 添加版本信息文件
            'manifest': '',  # -m, --manifest <FILE or XML> 添加manifest文件
            'additionalHooksDir': '',  # --additional-hooks-dir HOOKSPATH 指定用户的hook目录
            'runtimeHook': '',  # --runtime-hook RUNTIME_HOOKS 指定用户runtime-hook,如果设置了此参数，则runtime-hook会在运行main.py之前被运行
            'runtimeTmpdir': '',  # --runtime-tmpdir PATH 指定运行时的临时目录, 默认：使用系统临时目录
            'resource': '',  # -r, --resource RESOURCE
            'key': '',  # --key KEY pyi会存储字节码，指定加密字节码的key, 16位的字符串
        }

    def getCMD (self):

        cmd = str(pyinstaller_path)

        if not self.packageArgs['console'] or self.typeNum == 4:
            cmd = cmd + ' -w'

        if self.packageArgs['debug']:
            cmd = cmd + ' -d'

        if self.packageArgs['specPath']:
            cmd = cmd + ' --specpath ' + self.packageArgs['specPath']

        if self.packageArgs['importPath']:
            cmd = cmd + ' -p ' + self.packageArgs['importPath']

        if self.packageArgs['excludeModule']:
            cmd = cmd + ' –exclude-module ' + self.packageArgs['excludeModule']

        if self.packageArgs['hiddenImport']:
            for tmp in self.packageArgs['hiddenImport']:
                cmd = cmd + ' --hiddenimport ' + tmp

        if self.packageArgs['iconPath']:
            cmd = cmd + ' -i ' + self.packageArgs['iconPath']

        if self.packageArgs['workpath']:
            cmd = cmd + ' --workpath ' + self.packageArgs['workpath']

        if self.packageArgs['logLevel'] != 'INFO':
            cmd = cmd + ' --log-level ' + self.packageArgs['logLevel']

        if self.packageArgs['outType'] == 'FILE':
            cmd = cmd + ' -F'

        if self.packageArgs['outName']:
            cmd = cmd + ' -n ' + self.packageArgs['outName']

        if self.packageArgs['distpath']:
            cmd = cmd + ' --distpath ' + self.packageArgs['distpath']
        else:
            cmd = cmd + ' --distpath ' + self.cacheOutPath
            self.packageArgs['distpath'] = self.cacheOutPath

        if self.packageArgs['addData']:
            for tmp in self.packageArgs['addData']:
                cmd = cmd + ' --add-data ' + tmp

        if self.packageArgs['addBinary']:
            pass

        if self.packageArgs['isClean']:
            cmd = cmd + ' --clean'

        if self.packageArgs['encode']:
            cmd = cmd + ' -a'

        if self.packageArgs['isCover']:
            cmd = cmd + ' -y'

        if self.packageArgs['upxDir']:
            cmd = cmd + ' --upx-dir ' + self.packageArgs['upxDir']

        if self.packageArgs['versionFile']:
            cmd = cmd + ' --version-file ' + self.packageArgs['versionFile']

        if self.packageArgs['manifest']:
            cmd = cmd + ' -m ' + self.packageArgs['manifest']

        if self.packageArgs['additionalHooksDir']:
            pass

        if self.packageArgs['runtimeHook']:
            pass

        if self.packageArgs['runtimeTmpdir']:
            pass

        return cmd

    def run(self):
        cmd = self.getCMD()

        cmd = cmd + ' ' + self.mainFile
        cmd = 'cd /d ' + self.projectFolder + ' && ' + cmd
        print(cmd)

        subprocess.run(cmd, shell=True)

        if self.packageArgs['outName']:
            if self.typeNum == 4:
                tmp = 'cd /d ' + self.projectFolder + ' && ' + 'move ' + self.packageArgs['distpath'] + '\\' +self.packageArgs['outName'] + '.exe'\
                      + ' ' + self.packageArgs['distpath'] + '\\"' + self.packageArgs['outName'] + '_' + self.computer_digits + '_' + self.now + '.exe"'
            else:
                tmp = 'cd /d ' + self.projectFolder + ' && ' + 'move ' + self.packageArgs['distpath'] + '\\' + self.packageArgs['outName'] + '.exe' \
                      + ' ' + self.packageArgs['distpath'] + '\\"' + self.packageArgs['outName'] + '_' + Type[self.typeNum] + self.computer_digits + '_' + self.now + '.exe"'
        else:
            if self.typeNum == 4:
                tmp = 'cd /d ' + self.projectFolder + ' && ' + 'move ' + self.packageArgs['distpath'] + '\\' + self.mainFile.replace('.py', '.exe') \
                      + ' ' + self.packageArgs['distpath'] + '\\"' + self.mainFile.replace('.py', '') + '_' + self.computer_digits + '_' + self.now + '.exe"'
            else:
                tmp = 'cd /d ' + self.projectFolder + ' && ' + 'move ' + self.packageArgs['distpath'] + '\\' + self.mainFile.replace('.py', '.exe') \
                      + ' ' + self.packageArgs['distpath'] + '\\"' + self.mainFile.replace('.py', '') + '_' + Type[self.typeNum] + self.computer_digits + '_' + self.now + '.exe"'

        subprocess.run(tmp, shell=True)

        if self.packageArgs['isClean']:
            if self.packageArgs['outName']:
                subprocess.run('cd /d ' + self.projectFolder + ' && ' + "RD /Q /S " + "build\\" + self.packageArgs['outName'], shell=True)
            else:
                subprocess.run('cd /d ' + self.projectFolder + ' && ' + "RD /Q /S " + "build\\" + self.mainFile.replace('.py', ''), shell=True)
