#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Author  : yyxzz
# @Software: PyCharm
# @Time    : 2020/8/20 13:58

import os
from chardet import detect
from misc.color import Colors
from misc.encoding import Encode

class FileOPT:
    def __init__(self, cmd, clientSocket, sendBufferSize = 4096, recvBufferSize = 8192):
        self.cmd = cmd
        self.clientSocket = clientSocket
        self.sendBufferSize = sendBufferSize
        self.recvBufferSize = recvBufferSize
        # self.uploadFileLocalPath = r".\fileUpload"
        self.downloadFileLocalPath = r".\fileDownload"

    # 上传文件
    def fileUpload(self):
        if "\\" not in self.cmd.lstrip("upload").strip():
            localFilePath = ".\\" + self.cmd.lstrip("upload").strip()
        else:
            localFilePath = self.cmd.lstrip("upload").strip()
        # 输入文件合法性判断
        localFileName = localFilePath.split("\\")[-1]
        # 本地校验
        if not self.checkFile(localFilePath):
            self.clientSocket.send(self.cmd[:5].encode(Encode.encoding))
            return -1
        with open(localFilePath, "rb") as r:
                binData = r.read()
        self.clientSocket.send(localFileName.encode(Encode.encoding))
        resultCode = self.clientSocket.recv(self.recvBufferSize).decode(Encode.encoding)
        if resultCode == "1":
            self.clientSocket.send(binData)
        if resultCode == "0":
            print(self.clientSocket.recv(self.recvBufferSize).decode(Encode.encoding))
            while True:
                choice = input("Input Choice：g(go on covering)/m(make new file)/q(quit upload) > ").lower()
                if choice == "g":
                    self.clientSocket.send((choice + " ..").encode(Encode.encoding))
                    self.clientSocket.send(binData)
                elif choice == "m":
                    while True:
                        newFileName = input("Input New File Name：")
                        self.clientSocket.send((choice + " " + newFileName).encode(Encode.encoding))
                        resultCode = self.clientSocket.recv(self.recvBufferSize).decode(Encode.encoding)
                        if resultCode == "1":
                            break
                        print(self.clientSocket.recv(self.recvBufferSize).decode(Encode.encoding))
                    self.clientSocket.send(binData)
                elif choice == "q":
                    self.clientSocket.send((choice + " ..").encode(Encode.encoding))
                    print(Colors.YELLOW + "[!] Stop Upload Successfully !" + Colors.END)
                    return
                else:
                    print(Colors.RED + "[-] Input ERROR !" + Colors.END)
                    continue
                break
        result = self.clientSocket.recv(self.recvBufferSize).decode(Encode.encoding)
        print(result)

    # 下载文件
    def fileDownload(self):
        self.clientSocket.send((self.cmd).encode(Encode.encoding))
        resultCode = self.clientSocket.recv(self.recvBufferSize).decode(Encode.encoding)
        if resultCode == "findERROR":
            print(Colors.RED + "[-] No Such File ：%s" % (self.cmd[9:]) + Colors.END)
            return
        if resultCode == "openERROR":
            print(Colors.RED + "[-] Target File Open Failed , Maybe Do Not Have Permission !" % (self.cmd[9:]) + Colors.END)
            return
        recvFileName = self.clientSocket.recv(self.recvBufferSize).decode(Encode.encoding)
        binData = self.clientSocket.recv(self.recvBufferSize)
        targetFile = self.downloadFileLocalPath + "\\" + recvFileName   # 下载相对路径
        if not os.path.isdir(self.downloadFileLocalPath):
            os.mkdir(self.downloadFileLocalPath)
        if not os.path.isfile(targetFile):
            self.createFile(recvFileName, binData)
            return 0
        # 已存在同名文件，执行以下可选操作
        msg = Colors.YELLOW + "[!] The File Already Exists：%s " %(os.path.abspath(targetFile)) + Colors.END
        print(msg)
        while True:
            choice = input("Input Choice：g(go on covering)/m(make new file)/q(quit download) > ").lower()
            if choice == "g":
                self.createFile(recvFileName, binData)
            elif choice == "m":
                while True:
                    newFileName = input("Input New File Name：")
                    checkResult = self.checkLocalFile(newFileName)
                    if checkResult != "The File Already Exists":
                        break
                    targetFile = self.downloadFileLocalPath + "\\" + newFileName
                    print(Colors.YELLOW + "[!] The File Already Exists：%s " % (os.path.abspath(targetFile)) + Colors.END)
                self.createFile(newFileName, binData)
            elif choice == "q":
                print(Colors.YELLOW + "[!] Stop Download Successfully !" + Colors.END)
            else:
                print(Colors.RED + "[-] Input ERROR !" + Colors.END)
                continue
            return

    # 上传模块调用
    # 本地文件校验
    def checkFile(self, localFilePath):
        # 判断本地文件是否存在
        if not os.path.isfile(localFilePath):
            print(Colors.RED + "[-] No Such File ：%s" % (localFilePath) + Colors.END)
        else:
            try:
                # 文件读取权限校验
                with open(localFilePath, "rb") as r:
                    return True
            except:
                print(Colors.RED + "[-] File Opening Failed !" + Colors.END)
        return False

    # 下载模块调用
    # 检查文件是否已经存在
    def checkLocalFile(self, FileName):
        newFileName = FileName
        filePath = self.downloadFileLocalPath + "\\" + newFileName
        if os.path.isfile(filePath):
            return "The File Already Exists"
        return newFileName

    # 下载模块调用
    # 创建文件并写入内容
    def createFile(self, FileName, binData):
        targetFile = self.downloadFileLocalPath + "\\" + FileName  # 下载文件的相对路径
        fileEncoding = detect(binData)["encoding"]
        try:
            with open(targetFile, "w", encoding=fileEncoding) as w:
                w.writelines(binData.decode(fileEncoding))
                print(Colors.GREEN + "[+] Download Successfully ：%s" % (os.path.abspath(targetFile)) + Colors.END)
        except:
            print(Colors.RED + "[-] File Opening Failed ：%s" % (os.path.abspath(targetFile)) + Colors.END)
