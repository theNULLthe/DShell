#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Author  : yyxzz
# @Software: PyCharm
# @Time    : 2020/8/18 16:57

import os
from chardet import detect
from misc.color import Colors
from misc.encoding import Encode

class FileOPT:
    def __init__(self, client, sendBufferSize = 4096, recvBufferSize = 8192):
        self.client = client
        self.sendBufferSize = sendBufferSize
        self.recvBufferSize = recvBufferSize
        self.uploadPath = r".\fileDownload"

    # 上传
    def upload(self):
        localFileName = self.client.recv(self.recvBufferSize).decode(Encode.encoding)
        if localFileName == "uploa":
            return 0
        targetFile = self.uploadPath + "\\" + localFileName   # 上传相对路径
        if not os.path.isdir(self.uploadPath):
            os.mkdir(self.uploadPath)
        if not os.path.isfile(targetFile):
            self.client.send("1".encode(Encode.encoding))
            self.createFile(localFileName, self.uploadPath)
            return 0
        # 已存在同名文件，执行以下可选操作
        self.client.send("0".encode(Encode.encoding))
        msg = Colors.YELLOW + "[!] The File Already Exists：%s " %(os.path.abspath(targetFile)) + Colors.END
        self.client.send(msg.encode(Encode.encoding))
        choice = self.client.recv(self.recvBufferSize).decode(Encode.encoding)
        if choice.split()[0] == "m":
            FileName = choice.lstrip("m").strip()
            result = self.checkFile(FileName, self.uploadPath)
            targetFile = self.uploadPath + "\\" + FileName
            while result == "The File Already Exists":
                self.client.send("0".encode(Encode.encoding))
                self.client.send((Colors.YELLOW + "[!] The File Already Exists：%s " %(os.path.abspath(targetFile)) + Colors.END).encode(Encode.encoding))
                choice = self.client.recv(self.recvBufferSize).decode(Encode.encoding)
                FileName = choice.lstrip("m").strip()
                targetFile = self.uploadPath + "\\" + FileName
                result = self.checkFile(FileName, self.uploadPath)
            self.client.send("1".encode(Encode.encoding))
            newFileName = result
            self.createFile(newFileName, self.uploadPath)
        elif choice.split()[0] == "g":
            self.createFile(localFileName, self.uploadPath)
        elif choice.split()[0] == "q":
            return -1
        return -1

    # 下载
    def download(self):
        cmd = self.client.recv(self.recvBufferSize).decode(Encode.encoding)
        if "\\" not in cmd.lstrip("download").strip():
            localFilePath = ".\\" + cmd.lstrip("download").strip()
        else:
            localFilePath = cmd.lstrip("download").strip()
        # 本地校验
        if not self.checkLocalFile(localFilePath):
            return -1
        localFileAbsPath = os.path.abspath(localFilePath)
        localFileName = localFileAbsPath.split("\\")[-1]
        with open(localFileAbsPath, "rb") as r:
                binData = r.read()
        self.client.send(str(localFileName).encode(Encode.encoding))
        self.client.send(binData)

    # 上传模块调用
    # 检查文件是否已经存在
    def checkFile(self, FileName, targetPath):
        newFileName = FileName
        filePath = targetPath + "\\" + newFileName
        if os.path.isfile(filePath):
            return "The File Already Exists"
        return newFileName

    # 上传模块调用
    # 创建文件并写入内容
    def createFile(self, FileName, targetPath):
        targetFile = targetPath + "\\" + FileName  # 上传文件的相对路径
        binData = self.client.recv(self.recvBufferSize)
        fileEncoding = detect(binData)["encoding"]
        try:
            with open(targetFile, "w", encoding=fileEncoding) as w:
                w.writelines(binData.decode(fileEncoding))
                self.client.send((Colors.GREEN + "[+] Upload Successfully ：%s" % (os.path.abspath(targetFile)) + Colors.END).encode(Encode.encoding))
        except:
            self.client.send((Colors.RED + "[-] File Opening Failed ：%s" % (os.path.abspath(targetFile)) + Colors.END).encode(Encode.encoding))

    # 下载模块调用
    # 判断本地文件是否存在
    def checkLocalFile(self, localFilePath):
        if not os.path.isfile(localFilePath):
            self.client.send("findERROR".encode(Encode.encoding))
        else:
            try:
                # 文件读取权限校验
                with open(localFilePath, "rb") as r:
                    self.client.send("checkOK".encode(Encode.encoding))
                    return True
            except:
                self.client.send("openERROR".encode(Encode.encoding))
        return False

