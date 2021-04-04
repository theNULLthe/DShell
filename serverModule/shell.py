#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Author  : Cr4y0n
# @Software: PyCharm
# @Time    : 2020/8/20 13:57

from chardet import detect
from misc.color import Colors
from misc.encoding import Encode

class Shell:
    def __init__(self, clientSocket, sendBufferSize = 4096, recvBufferSize = 8192):
        self.clientSocket = clientSocket
        self.sendBufferSize = sendBufferSize
        self.recvBufferSize = recvBufferSize
        self.clientSocket.send("shell".encode(Encode.encoding))

    def shell(self):
        title = self.clientSocket.recv(self.recvBufferSize).decode(Encode.encoding)
        cmd = input(title.strip(r"\n"))
        self.clientSocket.send(cmd.encode(Encode.encoding))
        if cmd.lower() in ["quit", "q", "exit"]:
            print(Colors.RED  + "[-]" + Colors.END + " OS Shell Closed !")
            return 0
        else:
            result = self.clientSocket.recv(self.recvBufferSize)
            try:
                resultEncoding = detect(result)["encoding"]
                print(result.decode(resultEncoding))
            except:
                print(result.decode(Encode.encoding))
        return -1


