# iOS项目国际化改造

## 使用方式

1、传入路径，此处projectPath为绝对路径

`````
python3 AutoLocalizable.py [projectPath]
`````

2、直接将文件放到project工程目录下

```
python3 AutoLocalizable.py
```

3、将文件配置到xcode的**run script**上，每次编译直接执行

![image-20230227210609308](http://xingyajie.oss-cn-hangzhou.aliyuncs.com/uPic/image-20230227210609308.png)

## xib，sb文件处理

xib，sb文件在第一次开启Localization时会自动生成对应的strings文件并将用到的文本添加到strings中，但是后续添加控件时不会自动添加文本。后续可以使用**ibtool**命令来生成strings文件

```
ibtool [filePath] --generate-strings-file [resultPath]
```

新生成的strings文件与原strings文件合并

1. 在原文件中删除掉的控件ID信息前面加`//`注释掉
2. 新文件中添加的空间信息写入原strings文件中

## 纯代码文件处理

纯代码文件可以使用**genstrings**命令来生成strings文件

```
find . -name \*.m | xargs genstrings -o [resultPath]
```

新生成的strings文件与原strings文件合并，原理与上面相同







