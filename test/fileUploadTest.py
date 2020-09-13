#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Author  : yyxzz
# @Software: PyCharm
# @Time    : 2020/8/17 23:21

import os
from chardet import detect
from misc.color import Colors

class FileUpload:
    def checkFile(self, targetPath):
        while True:
            newFileName = input("Input New File Name：")
            filePath = targetPath + "\\" + newFileName
            if os.path.isfile(filePath):
                print(Colors.YELLOW + "[!] The File Already Exists：%s " %(os.path.abspath(newFileName)) + Colors.END)
                continue
            return newFileName

    def upload(self, localFileName, targetPath = r".\fileDownload"):
        if "\\" in localFileName:
            print(Colors.RED + "[-] Only Support Input Filename Which In fileUpload！" + Colors.END)
            return
        localFilePath = r".\fileUpload" + "\\" + localFileName # 本地文件相对路径
        targetFile = targetPath + "\\" + localFileName   # 上传目标相对路径
        try:
            with open(localFilePath, "rb") as r:
                binData = r.read()
                fileEncoding = detect(binData)["encoding"]
        except FileNotFoundError:
            print(Colors.RED + "[-] No Such File or Directory：%s" %(localFilePath) + Colors.END)
            return
        if not os.path.isdir(targetPath):
            os.mkdir(targetPath)
        if not os.path.isfile(targetFile):
            with open(targetFile, "w", encoding=fileEncoding) as w:
                w.writelines(binData.decode(fileEncoding))
                print(Colors.GREEN + "[+] Upload Successful ：%s" % (os.path.abspath(targetFile)) + Colors.END)
            return
        while True:
            print(Colors.YELLOW + "[!] The File Already Exists：%s " %(os.path.abspath(targetFile)) + Colors.END)
            choice = input("Input Choice：g(go on cover)/m(make new file)/q(quit upload) > ").lower()
            if choice == "g":
                with open(targetFile, "w", encoding=fileEncoding) as w:
                        w.writelines(binData.decode(fileEncoding))
                        print(Colors.GREEN + "Upload Successful ：%s" %(os.path.abspath(targetFile)) + Colors.END)
            elif choice == "m":
                newFileName = self.checkFile(targetPath)
                targetFile = targetPath + "\\" + newFileName
                with open(targetFile, "w", encoding=fileEncoding) as w:
                        w.writelines(binData.decode(fileEncoding))
                        print(Colors.GREEN + "[+] Upload Successful ：%s" %(os.path.abspath(targetFile)) + Colors.END)
            elif choice == "q":
                print(Colors.YELLOW + "[!] Stop Upload Successful！" + Colors.END)
            else:
                print(Colors.RED + "[-] Input ERROR！" + Colors.END)
                continue
            return




