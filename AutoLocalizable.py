#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import glob
import os
import sys


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


def findXibOrSbFilesIn(dir):
    resultPaths = []
    # 三个参数：1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
    for parent, dirnames, filenames in os.walk(dir):
        for filename in filenames:  # 输出文件信息
            if ('.xib' in filename) | ('.storyboard' in filename):
                filePath = os.path.join(parent)
                if filePath not in resultPaths:
                    resultPaths.append(filePath)
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
            sourceFile_list = glob.glob(sourceFilePathName)
            print('获得storyboard的具体文件')
            print(sourceFile_list)
            if len(sourceFile_list) == 0:
                print('目录：' + upperFilePath + '下，没有storyboard文件')
                return
            targetFilePath = upperFilePath + '/' + '*.lproj/*.strings'
            targetFile_list = glob.glob(targetFilePath)
            tempFile_Path = upperFilePath + '/' + 'TempStoryboard.strings'
            if len(targetFile_list) == 0:
                print('目录：' + upperFilePath + '下，没有strings文件')
                return
            for sourcePath in sourceFile_list:
                sourceprefix = extractFilePrefix(sourcePath)
                sourcename = extractFileName(sourcePath)
                print('-----')
                print(sourcePath)
                print(sourceprefix)
                print('目标文件名：' % sourcename)
                print('-----')


if __name__ == '__main__':
    main()
