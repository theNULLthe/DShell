#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Author  : Cr4y0n
# @Software: PyCharm
# @Time    : 2020/8/28 23:40

from random import choice
from misc.color import Colors

class Logo:
    def __init__(self):
        self.__logo1 = Colors.CYAN + r"""
 ___  ___  _         _  _ 
| . \/ __>| |_  ___ | || |
| | |\__ \| . |/ ._>| || |
|___/<___/|_|_|\___.|_||_|    (DanceShell)
""" + Colors.END

        self.__logo3 = Colors.RED + r"""
________    _________.__           .__  .__   
\______ \  /   _____/|  |__   ____ |  | |  |  
 |    |  \ \_____  \ |  |  \_/ __ \|  | |  |  
 |    `   \/        \|   Y  \  ___/|  |_|  |__
/_______  /_______  /|___|  /\___  >____/____/
        \/        \/      \/     \/               (DanceShell)
""" + Colors.END

    def printLogo(self):
        logoList = [self.__logo1, self.__logo3]
        author = Colors.GREEN + "\nAuthor: Cr4y0n\nVersion: v1.0" + Colors.END
        print(choice(logoList) + author)
