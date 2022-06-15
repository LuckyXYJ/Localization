#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import glob
import operator
import os

import MergeStringsFiles

TempStringsFile = 'temp.strings'


# 执行 ibtool 命令生成新的 strings 文件
def executeIbtoolShell(filePath, resultPath):
    cmdString = 'ibtool ' + filePath + ' --generate-strings-file ' + resultPath
    return os.system(cmdString) == 0


# 生成文件名
def extractFileName(file_path):
    seg = file_path.split('/')
    return seg[len(seg) - 1]


# 生成路径前缀
def extractFilePrefix(file_path):
    seg = file_path.split('/')
    length = len(seg)
    sufLen = len(seg[length - 2]) + len(seg[length - 1]) + 2
    return file_path[0:len(file_path) - sufLen]

def findXibOrSbFilesIn(dir):
    resultPaths = []
    # 三个参数：1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
    for parent, dirnames, filenames in os.walk(dir):
        for filename in filenames:  # 输出文件信息
            if ('.xib' in filename) | ('.storyboard' in filename):
                filePath = os.path.join(parent)
                fullFilePath = filePath + '/' + filename
                if fullFilePath not in resultPaths:
                    resultPaths.append(fullFilePath)
    return resultPaths

def dealXibOrSbFilePath(path):
    dragAndDropFiles = findXibOrSbFilesIn(path)
    for path in dragAndDropFiles:
        fileFullName = extractFileName(path)
        fileShortName = fileFullName.split('.')[0]
        preFilePath = extractFilePrefix(path)
        tempResultPath = preFilePath + '/' + TempStringsFile
        print('xib或sb文件路径 ==== ', path)
        if executeIbtoolShell(path, tempResultPath):
            resultFilePath = preFilePath + '/' + '*.lproj/*.strings'
            resultFileList = glob.glob(resultFilePath)
            for resultPath in resultFileList:
                resultName = extractFileName(resultPath)
                resultShortName = resultName.split('.')[0]
                if operator.eq(fileShortName, resultShortName):
                    MergeStringsFiles.dealWithStringsFile(resultPath, tempResultPath)
            os.remove(tempResultPath)
