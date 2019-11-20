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


def main():
    # sys.argv[1] 后面改为传参数方式
    filePath = '/Users/xyj/Private/思源/iOS/BaseProject'
    dragAndDropFiles = findXibOrSbFilesIn(filePath)
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
                    dealWithStringsFile(resultPath, tempResultPath)
            os.remove(tempResultPath)


if __name__ == '__main__':
    main()
