#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys

import DealCodeFile
import DealXibOrSbFile


def main():
    # sys.argv[1] 后面改为传参数方式
    if len(sys.argv) == 1:
        filePath = os.path.dirname(os.getcwd())
    else:
        filePath = sys.argv[1]
    DealXibOrSbFile.dealXibOrSbFilePath(filePath)
    DealCodeFile.dealCodeFilePath(filePath)


if __name__ == '__main__':
    main()
