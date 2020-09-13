#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Author  : yyxzz
# @Software: PyCharm
# @Time    : 2020/8/28 23:40

from random import choice
from misc.color import Colors

class Logo:
    def __init__(self):
        self.__logo1 = Colors.CYAN + r"""
 ______     ______   __             __   __   
|_   _ `. .' ____ \ [  |           [  | [  |  
  | | `. \| (___ \_| | |--.  .---.  | |  | |  
  | |  | | _.____`.  | .-. |/ /__\\ | |  | |  
 _| |_.' /| \____) | | | | || \__., | |  | |  
|______.'  \______.'[___]|__]'.__.'[___][___]     DanceShell
        """ + Colors.END

        self.__logo2 = Colors.GREEN + r"""
   ___     ___    _                 _       _    
  |   \   / __|  | |_      ___     | |     | |   
  | |) |  \__ \  | ' \    / -_)    | |     | |   
  |___/   |___/  |_||_|   \___|   _|_|_   _|_|_  
_|-----|_|-----|_|-----|_|-----|_|-----|_|-----| 
"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'     DanceShell
        """ + Colors.END

        self.__logo3 = Colors.BOLD + r"""
 ____   ___  _   _  ____  __    __   
(  _ \ / __)( )_( )( ___)(  )  (  )  
 )(_) )\__ \ ) _ (  )__)  )(__  )(__ 
(____/ (___/(_) (_)(____)(____)(____)    DanceShell
        """ + Colors.END

    def printLogo(self):
        logoList = [self.__logo1, self.__logo2, self.__logo3]
        print(choice(logoList))
