#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import codecs
import glob
import operator
import os
import re
import time
import chardet

TempStringsFile = 'temp.strings'
StringRegex = r'["](.*?)["]'

ResultParamRegex = r'["](.*?)["](\s*)=(\s*)["](.*?)["];'
CommentParamRegex = r'/(.*?)/'

def getTxtWithString(string):
    if string is None:
        return ''
    else:
        resultStringType = chardet.detect(string)
        resultStringText = string.decode(resultStringType['encoding'])
        return resultStringText


def constructCommentRegex(str):
    return CommentParamRegex + '\n' + str

def getCommentOfString(string_txt, suffix_string):
    commentRegex = constructCommentRegex(suffix_string)
    commentMatch = re.search(commentRegex, string_txt)
    commentString = ''
    if commentMatch:
        match = re.search(CommentParamRegex, commentMatch.group(0))
        if match:
            commentString = match.group(0)
    return commentString


def dealWithStringsFile(orgFilePath, tempFilePath):
    print('原strings文件        ===', orgFilePath)
    print('新生成strings文件     ===', tempFilePath)

    with codecs.open(tempFilePath, 'rb') as temp_file:
        tempString = temp_file.read()
        tempStringText = getTxtWithString(tempString)

        resultDict = {}
        commentDict = {}
        for iterator in re.finditer(ResultParamRegex, tempStringText):
            linestr = iterator.group(0)
            commentString = getCommentOfString(tempStringText, linestr)
            linematchs = re.findall(StringRegex, linestr)
            if len(linematchs) == 2:
                leftvalue = linematchs[0]
                rightvalue = linematchs[1]
                resultDict[leftvalue] = rightvalue
                commentDict[leftvalue] = commentString
            print('新字典 ----%s' % resultDict)
            print('不用的字典 ----%s' % commentDict)

    with codecs.open(orgFilePath, 'rb') as org_file:
        orgFileString = org_file.read()
        orgFileStringText = getTxtWithString(orgFileString)

        # print("读取的源文件内容：", orgFileStringText)
        originalDict = {}
        for iterator in re.finditer(ResultParamRegex, orgFileStringText):
            linestr = iterator.group(0)
            linematchs = re.findall(StringRegex, linestr)
            if len(linematchs) == 2:
                leftvalue = linematchs[0]
                rightvalue = linematchs[1]
                originalDict[leftvalue] = rightvalue

    for key in originalDict:
        if (key not in resultDict):
            print('=======', key)
            keystr = '"%s"' % key
            print(keystr)
            replacestr = '//' + keystr
            match = re.search(replacestr, orgFileStringText)
            if match is None:
                orgFileStringText = orgFileStringText.replace(keystr, replacestr)

    addHeader = True
    for key in resultDict:
        values = (key, resultDict[key])
        newline = ''
        if addHeader == True:
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            newline = '\n/// ----------------------------------------\n'
            newline += '/// AutoLocalizable            ' + timestamp + '\n'
            newline += '/// ----------------------------------------\n'
            addHeader = False
        newline += '\n' + commentDict[key]
        newline += '\n"%s" = "%s";\n' % values
        orgFileStringText += newline
    with codecs.open(orgFilePath, 'wb') as resultFile:
        resultFile.write(orgFileStringText.encode('UTF-8'))


#   读取source文件内容准备对比
#   对比文件添加或者删除内容
#   移除temp文件

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
        dealWithStringsFile(sourcePath, tempPathFile)
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
