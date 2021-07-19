#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Author  : Cr4y0n
# @Software: PyCharm
# @Time    : 2021/4/26
# @Github  : https://github.com/Cr4y0nXX

import time
from lib.dsPrint import *
from lib.dsSocket import *

def infoGather(clientSocket, clientAddress):
    DShellSend(clientSocket, "info")
    result = DShellRecv(clientSocket)
    print(result)
    outputPath = r"./output/hostInfo/"
    if not os.path.isdir(outputPath):
        os.mkdir(outputPath)
    date = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
    filename = f"{outputPath}{clientAddress[0]}_{date}.txt"
    try:
        with open(filename, "w", newline="") as f:
            f.write(result)
            successPrint(f"Result output: {filename}")
    except:
        pass