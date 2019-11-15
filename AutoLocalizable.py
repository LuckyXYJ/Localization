#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import glob
import os
import sys

TempStringsFile = 'temp.strings'


def executeIbtoolShell(filePath, resultPath):
    cmdString = 'ibtool ' + filePath + ' --generate-strings-file ' + resultPath
    return os.system(cmdString) == 0


# 生成文件名
def extractFileName(file_path):
    seg = file_path.split('/')
    lastindex = len(seg) - 1
    return seg[lastindex]


# 生成路径前缀
def extractFilePrefix(file_path):
    seg = file_path.split('/')
    lastindex = len(seg) - 1
    prefix = seg[lastindex].split('.')[0]
    return prefix


# 处理xib或sb文件，传入目标xib或sb文件path, 文件类型;
def dealWithXibOrSbFiles(targetFilePath, fileTypeName):
    baseStrIdx = targetFilePath.find('Base.lproj')
    if baseStrIdx < 0:
        return
    parentFilePath = targetFilePath[0:(baseStrIdx - 1)]

    filePathName = targetFilePath + '/*.' + fileTypeName

    targetFilePaths = glob.glob(filePathName)
    print('获得' + fileTypeName + '的具体文件')
    print(targetFilePaths)
    if len(targetFilePaths) == 0:
        print('目录：' + parentFilePath + '下，没有storyboard文件')
        return
    resultFilePath = parentFilePath + '/' + '*.lproj/*.strings'
    resultFile_list = glob.glob(resultFilePath)
    tempFile_Path = parentFilePath + '/' + 'TempStoryboard.strings'
    if len(targetFile_list) == 0:
        print('目录：' + parentFilePath + '下，没有strings文件')
        return
    for filePath in targetFilePaths:
        sourceprefix = extractFilePrefix(filePath)
        sourcename = extractFileName(filePath)
        print('-----')
        print(targetFilePath)
        print(sourceprefix)
        print('目标文件名：' % sourcename)
        print('-----')


def findXibOrSbFilesIn(dir):
    resultPaths = []
    # 三个参数：1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
    for parent, dirnames, filenames in os.walk(dir):
        for filename in filenames:  # 输出文件信息
            if ('.xib' in filename) | ('.storyboard' in filename):
                print(filename)
                filePath = os.path.join(parent)
                print(parent)
                print(filePath)
                fullFilePath = filePath + '/' + filename
                print(fullFilePath)
                if fullFilePath not in resultPaths:
                    resultPaths.append(fullFilePath)
    return resultPaths


def main():
    # sys.argv[1] 后面改为传参数方式
    filePath = '/Users/xyj/Private/思源/iOS/BaseProject'
    dragAndDropFiles = findXibOrSbFilesIn(filePath)
    print(dragAndDropFiles)
    for sourceFilePath in dragAndDropFiles:
        baseStrIdx = sourceFilePath.find('Base.lproj')
        if baseStrIdx >= 0:
            sourceFilePathName = sourceFilePath + '/*.storyboard'
            upperFilePath = sourceFilePath[0:(baseStrIdx - 1)]


if __name__ == '__main__':
    main()
