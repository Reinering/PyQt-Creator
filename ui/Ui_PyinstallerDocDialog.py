# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'PyinstallerDocDialog.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDialog, QGridLayout, QSizePolicy,
    QWidget)

from qfluentwidgets import TextEdit

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(1117, 719)
        font = QFont()
        font.setPointSize(14)
        Dialog.setFont(font)
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setSpacing(1)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(1, 1, 1, 1)
        self.TextEdit = TextEdit(Dialog)
        self.TextEdit.setObjectName(u"TextEdit")

        self.gridLayout.addWidget(self.TextEdit, 0, 0, 1, 1)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Pyinstaller \u6587\u6863", None))
        self.TextEdit.setHtml(QCoreApplication.translate("Dialog", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><title>\u914d\u7f6e\u6587\u4ef6</title><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Segoe UI','Microsoft YaHei','PingFang SC'; font-size:14px; font-weight:400; font-style:normal;\">\n"
"<h2 style=\" margin-top:16px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:180%;\"><span style=\" font-family:'Arial','sans-serif'; font-size:x-large; font-weight:700;\">pyinstaller \u53c2\u6570\u914d\u7f6e\u8bf4\u660e </span></h2>\n"
"<p style=\" margin-top:12px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:180%;\"><span style=\" fon"
                        "t-family:'YaHei'; font-size:16px;\">        </span><span style=\" font-family:'YaHei'; font-size:16px; font-weight:700;\">'console': True,</span><span style=\" font-family:'YaHei'; font-size:16px;\">  \u2003\u2003\u2003\u2003</span><span style=\" font-family:'YaHei'; font-size:16px; color:#808080;\"># [True, False] -w \u5173\u95ed\uff0c -c(\u9ed8\u8ba4) \u5f00\u542f \u5f00\u542f\u6216\u5173\u95ed\u663e\u793a\u63a7\u5236\u53f0 (\u53ea\u5bf9Windows\u6709\u6548)</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:180%;\"><span style=\" font-family:'YaHei'; font-size:16px;\">        </span><span style=\" font-family:'YaHei'; font-size:16px; font-weight:700;\">'debug': False,</span><span style=\" font-family:'YaHei'; font-size:16px;\">  \u2003\u2003\u2003\u2003</span><span style=\" font-family:'YaHei'; font-size:16px; color:#808080;\"># [True, False] -d [{all,imports,bootloader,noarchive} \u4ea7\u751fdebug\u7248\u672c\u7684"
                        "\u53ef\u6267\u884c\u6587\u4ef6</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:180%;\"><span style=\" font-family:'YaHei'; font-size:16px;\">        </span><span style=\" font-family:'YaHei'; font-size:16px; font-weight:700;\">'specPath': '',</span><span style=\" font-family:'YaHei'; font-size:16px;\">  \u2003\u2003\u2003\u2003</span><span style=\" font-family:'YaHei'; font-size:16px; color:#808080;\"># --specpath \u6307\u5b9aspec\u6587\u4ef6\u7684\u751f\u6210\u76ee\u5f55, \u5982\u679c\u6ca1\u6709\u6307\u5b9a, \u800c\u4e14\u5f53\u524d\u76ee\u5f55\u662fPyInstaller\u7684\u6839\u76ee\u5f55, \u4f1a\u81ea\u52a8\u521b\u5efa\u4e00\u4e2a\u7528\u4e8e\u8f93\u51fa(spec\u548c\u751f\u6210\u7684\u53ef\u6267\u884c\u6587\u4ef6)\u7684\u76ee\u5f55. \u5982\u679c\u6ca1\u6709\u6307\u5b9a, \u800c\u5f53\u524d\u76ee\u5f55\u4e0d\u662fPyInstaller\u7684\u6839\u76ee\u5f55, \u5219\u4f1a\u8f93\u51fa\u5230\u5f53\u524d\u7684\u76ee\u5f55\u4e0b</s"
                        "pan></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:180%;\"><span style=\" font-family:'YaHei'; font-size:16px;\">        </span><span style=\" font-family:'YaHei'; font-size:16px; font-weight:700;\">'importPath': '',</span><span style=\" font-family:'YaHei'; font-size:16px;\">  \u2003\u2003\u2003\u2003</span><span style=\" font-family:'YaHei'; font-size:16px; color:#808080;\"># -p, --path=DIR \u8bbe\u7f6e\u5bfc\u5165\u8def\u5f84 (\u548c\u4f7f\u7528PYTHONPATH\u6548\u679c\u76f8\u4f3c). \u53ef\u4ee5\u7528\u8def\u5f84\u5206\u5272\u7b26(Windows\u4f7f\u7528\u5206\u53f7, Linux\u4f7f\u7528\u5192\u53f7)\u5206\u5272, \u6307\u5b9a\u591a\u4e2a\u76ee\u5f55. \u4e5f\u53ef\u4ee5\u4f7f\u7528\u591a\u4e2a-p\u53c2\u6570\u6765\u8bbe\u7f6e\u591a\u4e2a\u5bfc\u5165\u8def\u5f84</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:180%;\"><span style=\""
                        " font-family:'YaHei'; font-size:16px;\">        </span><span style=\" font-family:'YaHei'; font-size:16px; font-weight:700;\">'excludeModule': [],</span><span style=\" font-family:'YaHei'; font-size:16px;\">  \u2003\u2003\u2003\u2003</span><span style=\" font-family:'YaHei'; font-size:16px; color:#808080;\"># --exclude-module \u9700\u8981\u6392\u9664\u7684module</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:180%;\"><span style=\" font-family:'YaHei'; font-size:16px;\">        </span><span style=\" font-family:'YaHei'; font-size:16px; font-weight:700;\">'hiddenImport': [],</span><span style=\" font-family:'YaHei'; font-size:16px;\">  \u2003\u2003\u2003\u2003</span><span style=\" font-family:'YaHei'; font-size:16px; color:#808080;\"># --hidden-import \u6253\u5305\u989d\u5916py\u5e93</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"
                        " line-height:180%;\"><span style=\" font-family:'YaHei'; font-size:16px;\">        </span><span style=\" font-family:'YaHei'; font-size:16px; font-weight:700;\">'iconPath': '',</span><span style=\" font-family:'YaHei'; font-size:16px;\">  \u2003\u2003\u2003\u2003</span><span style=\" font-family:'YaHei'; font-size:16px; color:#808080;\"># -i \u6307\u5b9a\u7a0b\u5e8f\u56fe\u6807 --icon=&lt;FILE.ICO&gt; \u5c06file.ico\u6dfb\u52a0\u4e3a\u53ef\u6267\u884c\u6587\u4ef6\u7684\u8d44\u6e90 --icon=&lt;FILE.EXE,N&gt; \u5c06file.exe\u7684\u7b2cn\u4e2a\u56fe\u6807\u6dfb\u52a0\u4e3a\u53ef\u6267\u884c\u6587\u4ef6\u7684\u8d44\u6e90 (\u53ea\u5bf9Windows\u7cfb\u7edf\u6709\u6548)</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:180%;\"><span style=\" font-family:'YaHei'; font-size:16px;\">        </span><span style=\" font-family:'YaHei'; font-size:16px; font-weight:700;\">'workpath': '',</span><span style=\" font-family:'YaHei'; fon"
                        "t-size:16px;\">  \u2003\u2003\u2003\u2003</span><span style=\" font-family:'YaHei'; font-size:16px; color:#808080;\"># --workpath WORKPATH \u751f\u6210\u8fc7\u7a0b\u4e2d\u7684\u4e2d\u95f4\u6587\u4ef6\u5b58\u653e\u76ee\u5f55\uff0c\u9ed8\u8ba4\uff1a\u5f53\u524d\u76ee\u5f55\u7684build\u6587\u4ef6\u5939\u5185</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:180%;\"><span style=\" font-family:'YaHei'; font-size:16px;\">        </span><span style=\" font-family:'YaHei'; font-size:16px; font-weight:700;\">'logLevel': 'INFO',</span><span style=\" font-family:'YaHei'; font-size:16px;\">  \u2003\u2003\u2003\u2003</span><span style=\" font-family:'YaHei'; font-size:16px; color:#808080;\"># --log-level LEVEL \u63a7\u5236\u7f16\u8bd1\u65f6pyi\u6253\u5370\u7684\u4fe1\u606f\uff0c\u4e00\u5171\u67096\u4e2a\u7b49\u7ea7\uff0c\u7531\u4f4e\u5230\u9ad8\u5206\u522b\u4e3aTRACE DEBUG INFO(\u9ed8\u8ba4) WARN ERROR CRITICAL\u3002\u4e5f\u5c31"
                        "\u662f\u9ed8\u8ba4\u60c5\u51b5\u4e0b\uff0c\u4e0d\u6253\u5370TRACE\u548cDEBUG\u4fe1\u606f</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:180%;\"><span style=\" font-family:'YaHei'; font-size:16px;\">        </span><span style=\" font-family:'YaHei'; font-size:16px; font-weight:700;\">'outType': 'FILE',</span><span style=\" font-family:'YaHei'; font-size:16px;\">  \u2003\u2003\u2003\u2003</span><span style=\" font-family:'YaHei'; font-size:16px; color:#808080;\"># ['FOLDER', 'FILE'] \u6253\u5305\u7684\u6587\u4ef6\u7c7b\u578b\uff1a-F \u4ea7\u751f\u4e00\u4e2a\u6587\u4ef6\u7528\u4e8e\u90e8\u7f72\uff1b-D \u4ea7\u751f\u4e00\u4e2a\u76ee\u5f55\u7528\u4e8e\u90e8\u7f72 (\u9ed8\u8ba4)</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:180%;\"><span style=\" font-family:'YaHei'; font-size:16px;\">        </span><span style=\" font-f"
                        "amily:'YaHei'; font-size:16px; font-weight:700;\">'outName': '',</span><span style=\" font-family:'YaHei'; font-size:16px;\">  \u2003\u2003\u2003\u2003</span><span style=\" font-family:'YaHei'; font-size:16px; color:#808080;\"># -n NAME \u6253\u5305\u7684\u6587\u4ef6\u540d \u53ef\u9009\u7684\u9879\u76ee\u540d\u5b57.\u5982\u679c\u7701\u7565,\u7b2c\u4e00\u4e2a\u811a\u672c\u7684\u4e3b\u6587\u4ef6\u540d\u5c06\u4f5c\u4e3aspec\u7684\u540d\u5b57</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:180%;\"><span style=\" font-family:'YaHei'; font-size:16px;\">        </span><span style=\" font-family:'YaHei'; font-size:16px; font-weight:700;\">'distpath': '',</span><span style=\" font-family:'YaHei'; font-size:16px;\">  </span><span style=\" font-family:'YaHei'; font-size:16px; color:#808080;\"># --distpath DIR \u751f\u6210\u6587\u4ef6\u5b58\u653e\u76ee\u5f55\uff0c\u5f53\u524d\u76ee\u5f55\u7684dist\u6587\u4ef6\u5939\u5185</spa"
                        "n></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:180%;\"><span style=\" font-family:'YaHei'; font-size:16px;\">        </span><span style=\" font-family:'YaHei'; font-size:16px; font-weight:700;\">'addData': [],</span><span style=\" font-family:'YaHei'; font-size:16px;\">  \u2003\u2003\u2003\u2003</span><span style=\" font-family:'YaHei'; font-size:16px; color:#808080;\"># --add-data &lt;SRC;DEST or SRC:DEST&gt; \u6253\u5305\u989d\u5916\u8d44\u6e90</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:180%;\"><span style=\" font-family:'YaHei'; font-size:16px;\">        </span><span style=\" font-family:'YaHei'; font-size:16px; font-weight:700;\">'addBinary': [],</span><span style=\" font-family:'YaHei'; font-size:16px;\">  \u2003\u2003\u2003\u2003</span><span style=\" font-family:'YaHei'; font-size:16px; color:#808080;\"># --ad"
                        "d-binary &lt;SRC;DEST or SRC:DEST&gt; \u6253\u5305\u989d\u5916\u7684\u4ee3\u7801</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:180%;\"><span style=\" font-family:'YaHei'; font-size:16px;\">        </span><span style=\" font-family:'YaHei'; font-size:16px; font-weight:700;\">'isClean': False,</span><span style=\" font-family:'YaHei'; font-size:16px;\">  \u2003\u2003\u2003\u2003</span><span style=\" font-family:'YaHei'; font-size:16px; color:#808080;\"># [True, False] --clean \u5728\u672c\u6b21\u7f16\u8bd1\u5f00\u59cb\u65f6\uff0c\u6e05\u7a7a\u4e0a\u4e00\u6b21\u7f16\u8bd1\u751f\u6210\u7684\u5404\u79cd\u6587\u4ef6,\u9ed8\u8ba4\uff1a\u4e0d\u6e05\u9664</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:180%;\"><span style=\" font-family:'YaHei'; font-size:16px;\">        </span><span style=\" font-family:'YaHei'; font-size:1"
                        "6px; font-weight:700;\">'encode': '',</span><span style=\" font-family:'YaHei'; font-size:16px;\">  \u2003\u2003\u2003\u2003</span><span style=\" font-family:'YaHei'; font-size:16px; color:#808080;\"># -a, --ascii \u4e0d\u5305\u542bunicode\u652f\u6301, \u9ed8\u8ba4\uff1a\u5c3d\u53ef\u80fd\u652f\u6301unicode</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:180%;\"><span style=\" font-family:'YaHei'; font-size:16px;\">        </span><span style=\" font-family:'YaHei'; font-size:16px; font-weight:700;\">'isCover': False,</span><span style=\" font-family:'YaHei'; font-size:16px;\">  \u2003\u2003\u2003\u2003</span><span style=\" font-family:'YaHei'; font-size:16px; color:#808080;\"># [True, False] -y, --noconfirm \u5982\u679cdist\u6587\u4ef6\u5939\u5185\u5df2\u7ecf\u5b58\u5728\u751f\u6210\u6587\u4ef6\uff0c\u5219\u4e0d\u8be2\u95ee\u7528\u6237\uff0c\u76f4\u63a5\u8986\u76d6, \u9ed8\u8ba4\uff1a\u8be2\u95ee\u662f\u5426\u8986"
                        "\u76d6</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:180%;\"><span style=\" font-family:'YaHei'; font-size:16px;\">        </span><span style=\" font-family:'YaHei'; font-size:16px; font-weight:700;\">'upxDir': '',</span><span style=\" font-family:'YaHei'; font-size:16px;\">  \u2003\u2003\u2003\u2003</span><span style=\" font-family:'YaHei'; font-size:16px; color:#808080;\"># --upx-dir UPX_DIR UPX\u5b9e\u7528\u7a0b\u5e8f\u7684\u8def\u5f84\uff08\u9ed8\u8ba4\u503c\uff1a\u641c\u7d22\u6267\u884c\u8def\u5f84\uff09</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:180%;\"><span style=\" font-family:'YaHei'; font-size:16px;\">        </span><span style=\" font-family:'YaHei'; font-size:16px; font-weight:700;\">'versionFile': '',</span><span style=\" font-family:'YaHei'; font-size:16px;\">  \u2003\u2003\u2003\u2003</span><spa"
                        "n style=\" font-family:'YaHei'; font-size:16px; color:#808080;\"># --version-file FILE \u6dfb\u52a0\u7248\u672c\u4fe1\u606f\u6587\u4ef6</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:180%;\"><span style=\" font-family:'YaHei'; font-size:16px;\">        </span><span style=\" font-family:'YaHei'; font-size:16px; font-weight:700;\">'manifest': '',</span><span style=\" font-family:'YaHei'; font-size:16px;\">  \u2003\u2003\u2003\u2003</span><span style=\" font-family:'YaHei'; font-size:16px; color:#808080;\"># -m, --manifest &lt;FILE or XML&gt; \u6dfb\u52a0manifest\u6587\u4ef6</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:180%;\"><span style=\" font-family:'YaHei'; font-size:16px;\">        </span><span style=\" font-family:'YaHei'; font-size:16px; font-weight:700;\">'additionalHooksDir': '',</span><span style=\" font-f"
                        "amily:'YaHei'; font-size:16px;\">  \u2003\u2003\u2003\u2003</span><span style=\" font-family:'YaHei'; font-size:16px; color:#808080;\"># --additional-hooks-dir HOOKSPATH \u6307\u5b9a\u7528\u6237\u7684hook\u76ee\u5f55</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:180%;\"><span style=\" font-family:'YaHei'; font-size:16px;\">        </span><span style=\" font-family:'YaHei'; font-size:16px; font-weight:700;\">'runtimeHook': '',</span><span style=\" font-family:'YaHei'; font-size:16px;\">  \u2003\u2003\u2003\u2003</span><span style=\" font-family:'YaHei'; font-size:16px; color:#808080;\"># --runtime-hook RUNTIME_HOOKS \u6307\u5b9a\u7528\u6237runtime-hook, \u5982\u679c\u8bbe\u7f6e\u4e86\u6b64\u53c2\u6570\uff0c\u5219runtime-hook\u4f1a\u5728\u8fd0\u884cmain.py\u4e4b\u524d\u88ab\u8fd0\u884c</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0"
                        "px; line-height:180%;\"><span style=\" font-family:'YaHei'; font-size:16px;\">        </span><span style=\" font-family:'YaHei'; font-size:16px; font-weight:700;\">'runtimeTmpdir': '',</span><span style=\" font-family:'YaHei'; font-size:16px;\">  \u2003\u2003\u2003\u2003</span><span style=\" font-family:'YaHei'; font-size:16px; color:#808080;\"># --runtime-tmpdir PATH \u6307\u5b9a\u8fd0\u884c\u65f6\u7684\u4e34\u65f6\u76ee\u5f55, \u9ed8\u8ba4\uff1a\u4f7f\u7528\u7cfb\u7edf\u4e34\u65f6\u76ee\u5f55</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:180%;\"><span style=\" font-family:'YaHei'; font-size:16px;\">        </span><span style=\" font-family:'YaHei'; font-size:16px; font-weight:700;\">'resource': '',</span><span style=\" font-family:'YaHei'; font-size:16px;\">  \u2003\u2003\u2003\u2003</span><span style=\" font-family:'YaHei'; font-size:16px; color:#808080;\"># -r, --resource RESOURCE</span></p>\n"
"<p style=\" "
                        "margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:180%;\"><span style=\" font-family:'YaHei'; font-size:16px;\">        </span><span style=\" font-family:'YaHei'; font-size:16px; font-weight:700;\">'key': '',</span><span style=\" font-family:'YaHei'; font-size:16px;\">  \u2003\u2003\u2003\u2003</span><span style=\" font-family:'YaHei'; font-size:16px; color:#808080;\"># --key KEY pyi\u4f1a\u5b58\u50a8\u5b57\u8282\u7801\uff0c\u6307\u5b9a\u52a0\u5bc6\u5b57\u8282\u7801\u7684key, 16\u4f4d\u7684\u5b57\u7b26\u4e32</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:180%;\"><span style=\" font-family:'YaHei'; font-size:16px;\">    </span><span style=\" font-size:14px;\"> </span></p></body></html>", None))
    # retranslateUi

