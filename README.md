# iOS老项目国际化改造

公司项目已经在线运行两年时间了， 突然接到领导通知需要做印尼市场，需要我们调研一下怎么样以最小的代价对项目进行改造，以适应印尼市场。


使用方式：

`python3 AutoLocalizable.py`

## xib，sb文件处理

xib，sb文件在第一次开启Localization时会自动生成对应的strings文件并将用到的文本添加到strings中，但是后续添加控件时不会自动添加文本。后续可以使用**ibtool**命令来生成strings文件

```
ibtool [filePath] --generate-strings-file [resultPath]
```

新生成的strings文件与原strings文件合并

1. 在原文件中删除掉的控件ID信息前面加`//`注释掉
2. 新文件中添加的空间信息写入原strings文件中



