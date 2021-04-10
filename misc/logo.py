#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Author  : Cr4y0n
# @Software: PyCharm
# @Time    : 2020/8/28 23:40

# from random import choice
from misc.color import Colors

class Logo:
    def __init__(self):
        self.__logo = Colors.CYAN + r"""
 ___  ___  _         _  _ 
| . \/ __>| |_  ___ | || |
| | |\__ \| . |/ ._>| || |
|___/<___/|_|_|\___.|_||_|    (DanceShell)
""" + Colors.END

    def printLogo(self):
        author = Colors.GREEN + "\nAuthor: Cr4y0n\nVersion: v4.0\n" + Colors.END
        print(self.__logo + author)
