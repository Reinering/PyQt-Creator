#






### i18n PyQt/PySide 国际化步骤

```
    1、在程序中使用 tr() 函数进行字符串的国际化
    2、每个Widget需要重写retranslateUi方法，注意使用designer生成的代码中已经包含了retranslateUi方法（需要删除），在其继承的类中重写即可
    3、使用 lupdate 进行国际化，lupdate 会扫描源代码中的 tr() 函数，并将其中的字符串提取到一个 .ts 文件中
    4、使用 Qt Linguist 编辑 .ts 文件，翻译成目标语言
    5、使用 lrelease 将 .ts 文件编译成 .qm 文件，供程序使用
    6、i18n文件中设置locales路径，加载翻译文件
    7、在UI中切换语言，调用i18n的switch_language方法

```