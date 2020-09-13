#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Author  : yyxzz
# @Software: PyCharm
# @Time    : 2020/8/20 13:57

from chardet import detect
from misc.color import Colors
from misc.encoding import Encode
from serverModule.fileOperation import FileOPT

class Shell:
    def __init__(self, clientSocket, sendBufferSize = 4096, recvBufferSize = 8192):
        self.clientSocket = clientSocket
        self.sendBufferSize = sendBufferSize
        self.recvBufferSize = recvBufferSize

    def shell(self):
        title = self.clientSocket.recv(self.recvBufferSize).decode(Encode.encoding)
        cmd = input(title.strip(r"\n"))
        self.clientSocket.send(cmd.encode(Encode.encoding))
        if cmd.lower() in ["quit", "q", "exit"]:
            print(Colors.RED  + "[-] Shell Closed !" + Colors.END)
            return 0
        elif cmd[:6].lower() == "upload":
            file = FileOPT(cmd, self.clientSocket)
            file.fileUpload()
        elif cmd[:8].lower() == "download":
            file = FileOPT(cmd, self.clientSocket)
            file.fileDownload()
        else:
            result = self.clientSocket.recv(self.recvBufferSize)
            try:
                resultEncoding = detect(result)["encoding"]
                print(result.decode(resultEncoding))
            except:
                print(result.decode(Encode.encoding))
        return -1