#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Author  : Sma11New
# @Software: PyCharm
# @Time    : 2020/8/28 23:40

# from random import choice
from misc.color import Colors

class Logo:
    def __init__(self):
        self.__logo = Colors.CYAN + r"""
                ____  _____ __         ____
               / __ \/ ___// /_  ___  / / /
              / / / /\__ \/ __ \/ _ \/ / / 
             / /_/ /___/ / / / /  __/ / /  
            /_____//____/_/ /_/\___/_/_/     (DanceShell)
""" + Colors.END

    def printLogo(self):
        author = Colors.GREEN + "\n\tAuthor: Sma11New\n\tVersion: v5.0\n" + Colors.END
        print(self.__logo + author)
