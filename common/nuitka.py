#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author: Reiner New
email: nbxlc@hotmail.com
"""

import os
import datetime


class NuitkaPackage:

    NUITKA_PARAMS = {
        'module': '',  # --module: 创建一个可导入的二进制扩展模块，而不是程序。默认关闭
        'standalone': True,  # [True, False] --standalone: 启用独立模式输出。这允许您将创建的二进制文件传输到其他机器上，而无需使用现有的Python安装。这也意味着它会变大。它隐含了"--follow-imports"和"--python-flag=no_site"选项。默认关闭
        'onefile': True,  # [True, False] --onefile: 在独立模式的基础上，启用单文件模式。这意味着不是创建一个文件夹，而是创建一个压缩的可执行文件。默认关闭
        'python-flag': '',  # [flag] --python-flag=FLAG: 使用Python标志。默认使用您运行Nuitka时使用的标志，这强制使用特定模式
        'python-debug': False,  # [True, False] --python-debug: 是否使用调试版本。默认使用您运行Nuitka时使用的版本，很可能是非调试版本。仅用于调试和测试目的
        'python-for-scons': '',  # [path] --python-for-scons=PATH: 当使用Python 3.4编译时，提供用于Scons的Python二进制文件路径
        'main': '',  # [path] --main=PATH: 如果指定一次，这将取代位置参数，即要编译的文件名。当多次给出时，它启用"multidist"（参见用户手册），允许您创建根据文件名或调用名称的二进制文件

        # 模块和包的包含控制
        'include-package': [],  # --include-package=PACKAGE: 包含整个包
        'include-module': [],  # --include-module=MODULE: 包含单个模块
        'include-plugin-directory': [],  # --include-plugin-directory=MODULE/PACKAGE: 也包含在该目录中找到的代码
        'include-plugin-files': [],  # --include-plugin-files=PATTERN: 包含匹配PATTERN的文件。
        'prefer-source-code': False,  # [True, False] --prefer-source-code: 对于已编译的扩展模块，如果同时存在源文件和扩展模块，通常使用扩展模块，但从可用源代码编译模块可能会获得更好的性能。

        # 导入模块的跟踪控制
        'follow-imports': False,  # [True, False] --follow-imports: 递归到所有导入的模块中
        'follow-import-to': '',  # --follow-import-to=MODULE/PACKAGE: 如果使用，跟踪到该模块，或如果是包，则跟踪到整个包
        'nofollow-import-to': '',  # --nofollow-import-to=MODULE/PACKAGE: 即使使用，也不要跟踪到该模块名称，或如果是包名称，则在任何情况下都不要跟踪到整个包
        'nofollow-imports': False,  # [True, False] --nofollow-imports: 完全不递归到任何导入的模块中
        'follow-stdlib': False,  # [True, False] --follow-stdlib: 也递归到标准库中导入的模块
        'onefile-tempdir-spec': '',  # --onefile-tempdir-spec=ONEFILE_TEMPDIR_SPEC: 在单文件模式下使用此文件夹进行解包
        'onefile-child-grace-time': '',
        # --onefile-child-grace-time=GRACE_TIME_MS: 当停止子进程时，例如由于CTRL-C或关机等，Python代码会收到"KeyboardInterrupt"，可以处理它以刷新数据。这是在以硬方式杀死子进程之前的时间量（毫秒）
        'onefile-no-compression': False,  # [True, False] --onefile-no-compression: 创建单文件时，禁用有效负载的压缩
        'onefile-as-archive': False,  # [True, False] --onefile-as-archive: 创建单文件时，使用可以用"nuitka-onefile-unpack"解包的归档格式

        # 数据文件
        'include-package-data': [],  # --include-package-data=PACKAGE: 包含给定包名称的数据文件
        'include-data-files': [],  # --include-data-files=DESC: 通过文件名在分发中包含数据文件
        'include-data-dir': [],  # --include-data-dir=DIRECTORY=DIRECTORY: 在分发中包含完整目录的数据文件
        'noinclude-data-files': [],  # --noinclude-data-files=PATTERN: 不包含匹配给定文件名模式的数据文件
        'include-onefile-external-data': [],  # --include-onefile-external-data=PATTERN: 在单文件二进制文件外部包含指定的数据文件模式
        'list-package-data': [],  # --list-package-data=LIST_PACKAGE_DATA: 输出为给定包名称找到的数据文件
        'include-raw-dir': [],  # --include-raw-dir=DIRECTORY: 在分发中完全包含原始目录

        # 元数据支持
        'include-distribution-metadata': '',  # --include-distribution-metadata=DISTRIBUTION: 包含给定分发名称的元数据信息

        # DLL文件
        'noinclude-dlls': [],  # --noinclude-dlls=PATTERN: 不包含匹配给定文件名模式的DLL文件
        'list-package-dlls': [],  # --list-package-dlls=LIST_PACKAGE_DLLS: 输出为给定包名称找到的DLL

        # 警告控制
        'warn-implicit-exceptions': False,  # [True, False] --warn-implicit-exceptions: 启用对编译时检测到的隐式异常的警
        'warn-unusual-code': False,  # [True, False] --warn-unusual-code: 启用对编译时检测到的异常代码的警告
        'assume-yes-for-downloads': False,  # [True, False] --assume-yes-for-downloads: 允许Nuitka在必要时下载外部代码
        'nowarn-mnemonic': '',  # --nowarn-mnemonic=MNEMONIC: 禁用给定助记符的警告

        # 编译后立即执行
        'run': False,  # [True, False] --run: 立即执行创建的二进制文件（或导入编译的模块）
        'debugger': '',  # [gdb, lldb, pdb] --debugger: 在调试器内执行，例如"gdb"或"lldb"，以自动获取堆栈跟踪

        # 编译选择
        'user-package-configuration-file': '',  # --user-package-configuration-file=YAML_FILENAME: 用户提供的包配置Yaml文件
        'full-compat': False,  # [True, False] --full-compat: 强制与CPython完全兼容
        'file-reference-choice': '',  # --file-reference-choice=MODE: 选择"file"将使用的值
        'module-name-choice': '',  # --module-name-choice=MODE: 选择"name"和"package"将使用的值
        'output-filename': '',  # --output-filename=FILENAME: 指定可执行文件应如何命名
        'output-dir': '',  # --output-dir=DIRECTORY: 指定中间和最终输出文件应放置的位置
        'remove-output': False,  # [True, False] --remove-output: 在生成模块或exe文件后删除构建目录
        'no-pyi-file': False,  # [True, False] --no-pyi-file: 不为Nuitka创建的扩展模块创建'.pyi'文件

        # 部署控制
        'deployment': False,  # [True, False]--deployment: 禁用旨在使发现兼容性问题更容易的代码
        'no-deployment-flag': '',  # --no-deployment-flag=FLAG: 保持部署模式，但选择性地禁用其部分

        # 环境控制
        'force-runtime-environment-variable': '',  # --force-runtime-environment-variable=VARIABLE_SPEC: 强制将环境变量设置为给定值

        # 调试功能
        'debug': False,  # [True, False]--debug: 执行所有可能的自检以查找Nuitka中的错误，不要用于生产
        'unstripped': False,  # [True, False] --unstripped: 在结果对象文件中保留调试信息，以便更好地与调试器交互
        'profile': False,  # [True, False] --profile: 启用基于vmprof的时间消耗分析。目前不工作
        'internal-graph': False,  # [True, False] --internal-graph: 创建优化过程内部的图表，不要用于整个程序，只用于小型测试用例
        'trace-execution': False,  # [True, False] --trace-execution: 跟踪执行输出，在执行代码行之前输出它
        'recompile-c-only': False,  # [True, False]--recompile-c-only: 这不是增量编译，仅用于Nuitka开发
        'xml': '',  # --xml=XML_FILENAME: 以XML形式将内部程序结构、优化结果写入给定文件名
        'experimental': '',  # --experimental=FLAG: 使用声明为"实验性"的功能
        'low-memory': False,  # [True, False] --low-memory: 尝试使用更少的内存
        'create-environment-from-report': '',  # --create-environment-from-report=CREATE_ENVIRONMENT_FROM_REPORT: 从给定的报告文件创建新的虚拟环境
        'generate-c-only': False,  # [True, False] --generate-c-only: 仅生成C源代码，不编译为二进制或模块

        # 后端C编译器
        'clang': False,  # [True, False]--clang: 强制使用clang
        'mingw64': False,  # [True, False] --mingw64: 在Windows上强制使用MinGW64
        'msvc': '',  # --msvc=MSVC_VERSION: 在Windows上强制使用特定MSVC版本
        'jobs': None,  # --jobs=N: 指定允许的并行C编译器作业数
        'lto': '',  # [yes, no]--lto=choice: 使用链接时优化（MSVC, gcc, clang））
        'static-libpython': '',  # --static-libpython=choice: 使用Python的静态链接库
        'cf-protection': '',  # --cf-protection=PROTECTION_MODE: 这个选项是gcc特有的

        # 缓存控制
        'disable-cache=': '',  # --disable-cache=DISABLED_CACHES: 禁用选定的缓存
        'clean-cache': '',  # --clean-cache=CLEAN_CACHES: 在执行之前清理给定的缓存
        'disable-bytecode-cache': False,  # [True, False] --disable-bytecode-cache: 不重用模块的依赖分析结果
        'disable-ccache': False,  # [True, False] --disable-ccache: 不尝试使用ccache（gcc, clang等）或clcache（MSVC, clangcl
        'disable-dll-dependency-cache': False,  # [True, False] --disable-dll-dependency-cache: 禁用依赖性walker缓存
        'force-dll-dependency-cache-update': False,  # [True, False] --force-dll-dependency-cache-update: 强制更新依赖性walker缓存

        # PGO编译
        'pgo': False,  # [True, False] --pgo: 启用C级别的配置文件引导优化（PGO）
        'pgo-args': '',  # --pgo-args=PGO_ARGS: 在配置文件引导优化的情况下传递的参数
        'pgo-executable': '',  # --pgo-executable=PGO_EXECUTABLE: 收集配置文件信息时要执行的命令
        'report': '',  # --report=REPORT_FILENAME: 在XML输出文件中报告模块、数据文件、编译、插件等详细信息
        'report-diffable': False,  # [True, False] --report-diffable: 以可比较的形式报告数据，即没有每次运行都会变化的时间或内存使用值
        'report-user-provided': '',  # --report-user-provided=KEY_VALUE: 报告来自您的数据
        'report-template': '',  # --report-template=REPORT_DESC: 通过模板报告
        'quiet': False,  # [True, False] --quiet: 禁用所有信息输出，但显示警告
        'show-scons': False,  # [True, False] --show-scons: 以详细信息运行C构建后端Scons
        'no-progressbar': False,  # [True, False] --no-progressbar: 禁用进度条
        'show-progress': False,  # [True, False] --show-progress: 过时：提供进度信息和统计
        'show-memory': False,  # [True, False] --show-memory: 提供内存信息和统计
        'show-modules': False,  # [True, False] --show-modules: 提供包含的模块和DLL的信息
        'show-modules-output': '',  # --show-modules-output=PATH: 输出'--show-modules'的位置
        'verbose': True,  # [True, False] --verbose: 输出所采取行动的详细信息，特别是在优化中
        'verbose-output': '',  # --verbose-output=PATH: '--verbose'的输出位置

        # 通用操作系统控制
        'windows-console-mode': 'disable',  # [force, disable, attach] --windows-console-mode=CONSOLE_MODE: 选择要使用的控制台模式
        'force-stdout-spec': '',  # --force-stdout-spec=FORCE_STDOUT_SPEC: 强制程序的标准输出到此位置
        'force-stderr-spec': '',  # --force-stderr-spec=FORCE_STDERR_SPEC: 强制程序的标准错误到此位置。

        # windows特定控制
        'windows-icon-from-ico': '',  # --windows-icon-from-ico=ICON_PATH: 添加可执行文件图标 指定window 应用程序图标 ico/png 文件
        'windows-icon-template-exe': '',  # --windows-icon-from-exe=ICON_EXE_PATH: 从现有可执行文件复制可执行文件图标, 指定window 应用程序图标 ico/png 文件
        'onefile-windows-splash-screen-image': '',  # --onefile-windows-splash-screen-image=SPLASH_SCREEN_IMAGE: 为Windows和单文件模式编译时，在加载应用程序时显示此图像
        'windows-uac-admin': '',  # --windows-uac-admin: 请求Windows用户控制，以在执行时授予管理员权限
        'windows-uac-uiaccess': '',  # --windows-uac-uiaccess: 请求Windows用户控制，以强制仅从少数文件夹运行，远程桌面访问

        # macOS特定控制
        'macos-create-app-bundle': False,  # [True, False] --macos-create-app-bundle: 为macOS编译时，创建一个bundle而不是普通的二进制应用程序
        'macos-target-arch': '',  # --macos-target-arch=MACOS_TARGET_ARCH: 这应该在哪些架构上运行。
        'macos-app-icon': '',  # --macos-app-icon=ICON_PATH: 为应用程序bundle添加图标
        'macos-signed-app-name': '',  # --macos-signed-app-name=MACOS_SIGNED_APP_NAME: 用于macOS签名的应用程序名称
        'macos-app-name': '',  # --macos-app-name=MACOS_APP_NAME: 在macOS bundle信息中使用的产品名称
        'macos-app-mode': '',  # --macos-app-mode=MODE: 应用程序bundle的应用程序模式
        'macos-sign-identity': '',  # --macos-sign-identity=MACOS_APP_VERSION: 在macOS上签名时使用的身份
        'macos-sign-notarization': '',  # --macos-sign-notarization: 使用适当的TeamID身份进行公证签名
        'macos-app-version': '',  # --macos-app-version=MACOS_APP_VERSION: 在macOS bundle信息中使用的产品版本
        'macos-app-protected-resource': '',  # --macos-app-protected-resource=RESOURCE_DESC: 请求访问macOS受保护资源的权限

        # Linux特定控制
        'linux-icon': '',   # --linux-icon=ICON_PATH: 为单文件二进制文件添加可执行文件图标

        # 二进制版本信息
        'company-name': '',  # --company-name=COMPANY_NAME: 在版本信息中使用的公司名称
        'product-name': '',  # --product-name=PRODUCT_NAME: 在版本信息中使用的产品名称
        'file-version': '',  # --file-version=FILE_VERSION: 在版本信息中使用的文件版本
        'product-version': '',  # --product-version=PRODUCT_VERSION: 在版本信息中使用的产品版本
        'file-description': '',  # --file-description=FILE_DESCRIPTION: 在版本信息中使用的文件描述
        'copyright': '',    # --copyright=COPYRIGHT_TEXT: 在版本信息中使用的版权信息
        'trademarks': '',   # --trademarks=TRADEMARKS_TEXT: 在版本信息中使用的商标信息

        # 插件控制
        'enable-plugins': [],  # --enable-plugins=PLUGIN_NAME: 启用的插件
        'disable-plugins': [],  # --disable-plugins=PLUGIN_NAME: 禁用的插件
        'user-plugin': [],  # --user-plugin=PATH: 用户插件的文件名
        'plugin-list': False,  # [True, False] --plugin-list: 显示所有可用插件的列表并退出
        'plugin-no-detection': False,  # [True, False] --plugin-no-detection: 禁用插件检测机制
        'module-parameter': '',  # --module-parameter=MODULE_PARAMETERS: 提供模块参数
        'show-source-changes': '',  # --show-source-changes=SHOW_SOURCE_CHANGES: 显示对原始Python文件内容的源代码更改
        'noinclude-dask-mode': '',  # --noinclude-dask-mode=NOINCLUDE_DASK_MODE: 遇到'dask'导入时的处理方式
        'noinclude-numba-mode': '',  # --noinclude-numba-mode=NOINCLUDE_NUMBA_MODE: 遇到'numba'导入时的处理方式
        'noinclude-default-mode': '',  # --noinclude-default-mode=NOINCLUDE_DEFAULT_MODE: 为上述选项提供默认的"警告"值
        'noinclude-custom-mode': '',  # --noinclude-custom-mode=CUSTOM_CHOICES: 遇到特定导入时的处理方式
    }

    def __init__(self):
        self.projectFolder = os.getcwd()
        self.cacheDir = ''
        self.mainFile = "main.py"
        self.cacheOutPath = 'dist'

    def getCMD(self):
        now = datetime.datetime.now().strftime("%Y%m%d%H%M")

        cmd = ''
        #
        if self.NUITKA_PARAMS['module']:
            cmd += ' --module'

        if self.NUITKA_PARAMS['standalone']:
            cmd += ' --standalone'

        if self.NUITKA_PARAMS['onefile']:
            cmd += ' --onefile'

        if self.NUITKA_PARAMS['python-debug']:
            cmd += ' --python-debug'

        if self.NUITKA_PARAMS['python-for-scons']:
            cmd += ' --python-for-scons=' + self.NUITKA_PARAMS['python-for-scons']


        # 模块和包的包含控制
        if self.NUITKA_PARAMS['include-package']:
            for tmp in self.NUITKA_PARAMS['include-package']:
                cmd += ' --include-package=' + tmp

        if self.NUITKA_PARAMS['include-module']:
            for tmp in self.NUITKA_PARAMS['include-module']:
                cmd += ' --include-module=' + tmp

        if self.NUITKA_PARAMS['include-plugin-directory']:
            for tmp in self.NUITKA_PARAMS['include-plugin-directory']:
                cmd += ' --include-plugin-directory=' + tmp

        if self.NUITKA_PARAMS['include-plugin-files']:
            for tmp in self.NUITKA_PARAMS['include-plugin-files']:
                cmd += ' --include-plugin-files=' + tmp

        if self.NUITKA_PARAMS['prefer-source-code']:
            cmd += ' --prefer-source-code'


        # 导入模块的跟踪控制
        if self.NUITKA_PARAMS['follow-imports']:
            cmd += ' --follow-imports'

        if self.NUITKA_PARAMS['nofollow-imports']:
            cmd += ' --nofollow-imports'

        if self.NUITKA_PARAMS['follow-stdlib']:
            cmd += ' --follow-stdlib'

        if self.NUITKA_PARAMS['onefile-no-compression']:
            cmd += ' --onefile-no-compression'

        if self.NUITKA_PARAMS['onefile-as-archive']:
            cmd += ' --onefile-as-archive'

        # 数据文件
        if self.NUITKA_PARAMS['include-package-data']:
            for tmp in self.NUITKA_PARAMS['include-package-data']:
                cmd += ' --include-package-data=' + tmp

        if self.NUITKA_PARAMS['include-data-files']:
            for tmp in self.NUITKA_PARAMS['include-data-files']:
                cmd += ' --include-data-files=' + tmp

        if self.NUITKA_PARAMS['include-data-dir']:
            for tmp in self.NUITKA_PARAMS['include-data-dir']:
                cmd += ' --include-data-dir=' + tmp

        if self.NUITKA_PARAMS['noinclude-data-files']:
            for tmp in self.NUITKA_PARAMS['noinclude-data-files']:
                cmd += ' --noinclude-data-files=' + tmp

        if self.NUITKA_PARAMS['include-onefile-external-data']:
            for tmp in self.NUITKA_PARAMS['include-onefile-external-data']:
                cmd += ' --include-onefile-external-data=' + tmp

        if self.NUITKA_PARAMS['include-raw-dir']:
            for tmp in self.NUITKA_PARAMS['include-raw-dir']:
                cmd += ' --include-raw-dir=' + tmp

        # 元数据支持

        # DLL文件
        if self.NUITKA_PARAMS['noinclude-dlls']:
            for tmp in self.NUITKA_PARAMS['noinclude-dlls']:
                cmd += ' --noinclude-dlls=' + tmp

        if self.NUITKA_PARAMS['list-package-dlls=LIST_PACKAGE_DLLS']:
            for tmp in self.NUITKA_PARAMS['list-package-dlls=LIST_PACKAGE_DLLS']:
                cmd += ' --list-package-dlls=LIST_PACKAGE_DLLS=' + tmp

        # 警告控制
        if self.NUITKA_PARAMS['warn-implicit-exceptions']:
            cmd += ' --warn-implicit-exceptions'

        if self.NUITKA_PARAMS['warn-unusual-code']:
            cmd += ' --warn-unusual-code'

        if self.NUITKA_PARAMS['assume-yes-for-downloads']:
            cmd += ' --assume-yes-for-downloads'

        # 编译后立即执行
        if self.NUITKA_PARAMS['run']:
            cmd += ' --run'

        if self.NUITKA_PARAMS['debugger']:
            cmd += ' --debugger=' + self.NUITKA_PARAMS['debugger']

        # 编译选择
        if self.NUITKA_PARAMS['full-compat']:
            cmd += ' --full-compat'

        if self.NUITKA_PARAMS['output-filename']:
            cmd += ' --output-filename=' + self.NUITKA_PARAMS['output-filename']

        if self.NUITKA_PARAMS['output-dir']:
            cmd += ' --output-dir=' + self.NUITKA_PARAMS['output-dir']
        else:
            self.NUITKA_PARAMS['output-dir'] = self.cacheOutPath
            cmd += ' --output-dir=' + self.cacheOutPath

        if self.NUITKA_PARAMS['remove-output']:
            cmd += ' --remove-output'

        if self.NUITKA_PARAMS['no-pyi-file']:
            cmd += ' --no-pyi-file'


        # 部署控制
        if self.NUITKA_PARAMS['deployment']:
            cmd += ' --deployment'

        # 环境控制

        # 调试功能
        if self.NUITKA_PARAMS['debug']:
            cmd += ' --debug'

        if self.NUITKA_PARAMS['unstripped']:
            cmd += ' --unstripped'

        if self.NUITKA_PARAMS['profile']:
            cmd += ' --profile'

        if self.NUITKA_PARAMS['internal-graph']:
            cmd += ' --internal-graph'

        if self.NUITKA_PARAMS['trace-execution']:
            cmd += ' --trace-execution'

        if self.NUITKA_PARAMS['recompile-c-only']:
            cmd += ' --recompile-c-only'

        if self.NUITKA_PARAMS['low-memory']:
            cmd += ' --low-memory'

        if self.NUITKA_PARAMS['generate-c-only']:
            cmd += ' --generate-c-only'

        # 后端C编译器
        if self.NUITKA_PARAMS['clang']:
            cmd += ' --clang'

        if self.NUITKA_PARAMS['mingw64']:
            cmd += ' --mingw64'

        if self.NUITKA_PARAMS['lto'] == "yes":
            cmd += ' --lto=yes'



        # 缓存控制
        if self.NUITKA_PARAMS['disable-bytecode-cache']:
            cmd += ' --disable-bytecode-cache'

        if self.NUITKA_PARAMS['disable-ccache']:
            cmd += ' --disable-ccache'

        if self.NUITKA_PARAMS['disable-dll-dependency-cache']:
            cmd += ' --disable-dll-dependency-cache'

        if self.NUITKA_PARAMS['force-dll-dependency-cache-update']:
            cmd += ' --force-dll-dependency-cache-update'

        # PGO编译
        if self.NUITKA_PARAMS['quiet']:
            cmd += ' --quiet'

        if self.NUITKA_PARAMS['show-scons']:
            cmd += ' --show-scons'

        if self.NUITKA_PARAMS['no-progressbar']:
            cmd += ' --no-progressbar'

        if self.NUITKA_PARAMS['show-progress']:
            cmd += ' --show-progress'

        if self.NUITKA_PARAMS['show-memory']:
            cmd += ' --show-memory'

        if self.NUITKA_PARAMS['show-modules']:
            cmd += ' --show-modules'

        if self.NUITKA_PARAMS['show-modules-output']:
            cmd += ' --show-modules-output=' + self.NUITKA_PARAMS['show-modules-output']

        if self.NUITKA_PARAMS['verbose']:
            cmd += ' --verbose'

        if self.NUITKA_PARAMS['verbose-output']:
            cmd += ' --verbose-output=' + self.NUITKA_PARAMS['verbose-output']

        # 通用操作系统控制
        if self.NUITKA_PARAMS['windows-console-mode']:
            cmd += ' --windows-console-mode=' + self.NUITKA_PARAMS['windows-console-mode']

        # windows
        if self.NUITKA_PARAMS['windows-icon-from-ico']:
            cmd += ' --windows-icon-from-ico=' + self.NUITKA_PARAMS['windows-icon-from-ico']

        # macOS特定控制

        # Linux特定控制
        if self.NUITKA_PARAMS['linux-icon']:
            cmd += ' --linux-icon=' + self.NUITKA_PARAMS['linux-icon']

        # 二进制版本信息
        if self.NUITKA_PARAMS['company-name']:
            cmd += ' --company-name=' + self.NUITKA_PARAMS['company-name']

        if self.NUITKA_PARAMS['product-name']:
            cmd += ' --product-name=' + self.NUITKA_PARAMS['product-name']

        if self.NUITKA_PARAMS['file-version']:
            cmd += ' --file-version=' + self.NUITKA_PARAMS['file-version']

        if self.NUITKA_PARAMS['product-version']:
            cmd += ' --product-version=' + self.NUITKA_PARAMS['product-version']

        if self.NUITKA_PARAMS['file-description']:
            cmd += ' --file-description=' + self.NUITKA_PARAMS['file-description']

        if self.NUITKA_PARAMS['copyright']:
            cmd += ' --copyright=' + self.NUITKA_PARAMS['copyright']

        if self.NUITKA_PARAMS['trademarks']:
            cmd += ' --trademarks=' + self.NUITKA_PARAMS['trademarks']

        # 插件控制
        if self.NUITKA_PARAMS['enable-plugins']:
            for tmp in self.NUITKA_PARAMS['enable-plugins']:
                cmd += ' --enable-plugin=' + tmp

        if self.NUITKA_PARAMS['disable-plugins']:
            for tmp in self.NUITKA_PARAMS['disable-plugins']:
                cmd += ' --disable-plugins=' + tmp

        if self.NUITKA_PARAMS['user-plugin']:
            for tmp in self.NUITKA_PARAMS['user-plugin']:
                cmd += ' --user-plugin=' + tmp

        if self.NUITKA_PARAMS['plugin-list']:
            cmd += ' --plugin-list'

        if self.NUITKA_PARAMS['plugin-no-detection']:
            cmd += ' --plugin-no-detection'




        return cmd
