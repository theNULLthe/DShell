#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Author  : Cr4y0n
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

    # 上传文件
    def fileUpload(self):
        def printUploadResult(result):
            if result == "Success":
                print((Colors.GREEN + "[+]" + Colors.END + " Upload Successfully ：%s" % (remoteFile)))
            elif result == "Fail":
                print((Colors.RED + "[-]" + Colors.END + " Upload Failed ：%s（Maybe you have no access to write.）" % (
                    remoteFile)))
            else:
                print(Colors.YELLOW + "[!]" + Colors.END + " Something Error.")
        if not self.checkCMD(self.cmd)[0]:
            return 0
        self.cmd = self.checkCMD(self.cmd)[1]
        localFile = self.cmd.split()[1]
        remoteFile = self.cmd.split()[2]
        if "/" not in localFile:
            localFile = "./" + localFile
        if "/" not in remoteFile:
            remoteFile = "./" + remoteFile
        # 本地校验
        if not self.checkFile(localFile):
            return -1
        self.clientSocket.send(self.cmd.encode(Encode.encoding))
        resultCode = self.clientSocket.recv(self.recvBufferSize).decode(Encode.encoding)
        if resultCode == "1":
            with open(localFile, "rb") as r:
                    binData = r.read()
            self.clientSocket.send(binData)
            result = self.clientSocket.recv(self.recvBufferSize).decode(Encode.encoding)
            printUploadResult(result)
        if resultCode == "0":
            print(Colors.YELLOW + "[!]" + Colors.END + " The Remote File Already Exists.")
            choice = input("Do you wang to cover the remote file?(y/n) ").lower()
            if choice == "y":
                self.clientSocket.send("cover".encode(Encode.encoding))
                with open(localFile, "rb") as r:
                    binData = r.read()
                self.clientSocket.send(binData)
                result = self.clientSocket.recv(self.recvBufferSize).decode(Encode.encoding)
                printUploadResult(result)
            elif choice == "n":
                self.clientSocket.send("pass".encode(Encode.encoding))
            else:
                self.clientSocket.send("pass".encode(Encode.encoding))
                print(Colors.YELLOW + "[!]" + Colors.END + " Input Error.")

    # 下载文件
    def fileDownload(self):
        if not self.checkCMD(self.cmd)[0]:
            return 0
        self.cmd = self.checkCMD(self.cmd)[1]
        localFile = self.cmd.split()[2]
        remoteFile = self.cmd.split()[1]
        if "/" not in localFile:
            localFile = "./" + localFile
        if "/" not in remoteFile:
            remoteFile = "./" + remoteFile
        # 本地文件校验
        if not os.path.isfile(localFile):
            self.clientSocket.send((self.cmd).encode(Encode.encoding))
            resultCode = self.clientSocket.recv(self.recvBufferSize).decode(Encode.encoding)
            if resultCode == "findERROR":
                print(Colors.RED + "[-]" + Colors.END + " No Such File ：%s" % (remoteFile))
                return 0
            if resultCode == "openERROR":
                print(Colors.RED + "[-]" + Colors.END + " The Remote File Open Failed , Maybe Do Not Have Permission !")
                return 0
            binData = self.clientSocket.recv(self.recvBufferSize)
            self.createFile(localFile, binData)
            return 0
        print(Colors.YELLOW + "[!]" + Colors.END + " The Local File Already Exists.")
        choice = input("Do you wang to [COVER] the file?(y/n) ").lower()
        if choice == "y":
            self.clientSocket.send((self.cmd).encode(Encode.encoding))
            resultCode = self.clientSocket.recv(self.recvBufferSize).decode(Encode.encoding)
            if resultCode == "findERROR":
                print(Colors.RED + "[-]" + Colors.END + " No Such Remote File ：%s" % (remoteFile))
                return 0
            if resultCode == "openERROR":
                print(Colors.RED + "[-]" + Colors.END + " The Remote File Open Failed , Maybe Do Not Have Permission !")
                return 0
            binData = self.clientSocket.recv(self.recvBufferSize)
            self.createFile(localFile, binData)
        elif choice == "n":
            pass
        else:
            print(Colors.YELLOW + "[!]" + Colors.END + " Input Error.")

    # 本地文件校验
    def checkFile(self, fileName):
        # 判断本地文件是否存在
        if not os.path.isfile(fileName):
            print(Colors.RED + "[-]" + Colors.END +  " No Such Local File ：%s" % (fileName))
        else:
            try:
                # 文件读取权限校验
                with open(fileName, "rb") as r:
                    return True
            except:
                print(Colors.RED + "[-]" + Colors.END + " File Opening Failed !")
        return False

    # 创建文件并写入内容
    def createFile(self, fileName, binData):
        fileEncoding = detect(binData)["encoding"]
        try:
            with open(fileName, "w", encoding=fileEncoding) as w:
                w.writelines(binData.decode(fileEncoding))
                print(Colors.GREEN + "[+]" + Colors.END + " Download Successfully ：%s" % (fileName))
        except:
            print(Colors.RED + "[-]" + Colors.END + " File Opening Failed ：%s" % (fileName))

    # 上传下载命令合理性校验
    def checkCMD(self, cmd):
        # 合理性
        if len(cmd.split()) not in [2, 3]:
            print(Colors.YELLOW + "[!]" + Colors.END + " Input Error.")
            return False, cmd
        # 未指定第三个参数，进行补充
        if len(cmd.split()) == 2:
            if "/" in cmd.split()[1]:
                cmd += " " + cmd.split()[1].split("/")[-1]
            else:
                cmd += " " + cmd.split()[1]
        return True, cmd
