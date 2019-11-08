#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys


def main():
    # sys.argv[1] 后面改为传参数方式
    filePath = '/Users/xyj/Private/思源/iOS/BaseProject'

    sourceFilePaths = []
    # 三个参数：1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
    for parent, dirnames, filenames in os.walk(filePath):
        for filename in filenames:  # 输出文件信息
            print(filename)
            if ('.xib' in filename) | ('.storyboard' in filename):
                filePath = os.path.join(parent)
                if filePath not in sourceFilePaths:
                    sourceFilePaths.append(filePath)
    print('sourceFilePaths --- %s' % sourceFilePaths)


# return sourceFilePaths


if __name__ == '__main__':
    main()
