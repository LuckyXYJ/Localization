#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import operator
import os

import MergeStringsFiles


def generateCodeFiles(projectPath):
    print("代码国际化")
    # 	生成temp文件
    tempPath = 'tempLocalizableStringsFilePath'
    cmdCD = 'cd ' + projectPath
    cmdMKDIR = 'mkdir ' + tempPath

    tempFilePath = projectPath + '/' + tempPath
    if os.path.exists(tempFilePath):
        cmdString = cmdCD + '&&' + 'find . -name \*.m | xargs genstrings -o ' + tempPath
    else:
        cmdString = cmdCD + '&&' + cmdMKDIR + '&&' + 'find . -name \*.m | xargs genstrings -o ' + tempPath

    if os.system(cmdString) == 0:
        return tempFilePath
    else:
        return 1


# 生成代码文件
def generateCodeLocalizableFile(sourcePaths, projectPath):
    tempPath = generateCodeFiles(projectPath)
    if tempPath == 1:
        return
    nameString = 'Localizable.strings'
    tempPathFile = tempPath + '/' + nameString
    for sourcePath in sourcePaths:
        MergeStringsFiles.dealWithStringsFile(sourcePath, tempPathFile)
    os.remove(tempPathFile)


# 根据查找所有含有Localizable的文件路径
def findLocalizableFilesIn(dir):
    resultPaths = []
    # 三个参数：1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
    for parent, dirnames, filenames in os.walk(dir):
        for filename in filenames:
            if operator.eq('Localizable.strings', filename):
                filePath = os.path.join(parent) + '/' + filename
                if filePath not in resultPaths:
                    resultPaths.append(filePath)
    # print('resultPaths', sourceFilePaths)
    return resultPaths


def dealCodeFilePath(path):
    localizableFiles = findLocalizableFilesIn(path)
    generateCodeLocalizableFile(localizableFiles, path)
