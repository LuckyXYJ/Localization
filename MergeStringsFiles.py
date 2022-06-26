#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import codecs
import re
import time
import chardet

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


# 合并strings文件，orgFilePath原文件，tempFilePath临时文件，将临时文件合并到源文件内
def dealWithStringsFile(orgFilePath, tempFilePath):

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
            keystr = '"%s"' % key
            replacestr = '//' + keystr
            match = re.search(replacestr, orgFileStringText)
            if match is None:
                orgFileStringText = orgFileStringText.replace(keystr, replacestr)

    addHeader = True
    for key in resultDict:
        values = (key, resultDict[key])
        if (key not in originalDict):
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
