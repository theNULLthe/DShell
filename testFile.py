#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Author  : yyxzz
# @Software: PyCharm
# @Time    : 2020/8/18 15:42

from test.fileUploadTest import FileUpload

if __name__ == "__main__":
    FileUpload = FileUpload()
    fileName = input("filename：")
    FileUpload.upload(fileName)
