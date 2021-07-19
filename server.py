#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Author  : Cr4y0n
# @Software: PyCharm
# @Time    : 2021/4/8 23:42

import os
import sys
from misc.logo import Logo
from misc.color import Colors
from serverModule.args import serverParseArgs
from serverModule.vulScan import vulDic
from serverModule.tool import toolDic

vulDicData = vulDic()
toolDicData = toolDic()

# 根据关键字执行相应模块
def executeModule(choice, keyWord, moduleName):
    args = choice[len(keyWord):]

    if keyWord == "vulscan":
        args = choice.split(choice.split()[1])[1]
        os.chdir(r"./vulScan")
    elif keyWord == "tool":
        args = choice.split(choice.split()[1])[1]
        os.chdir(r"./tools")
    else:
        os.chdir(r"./serverModule")
    cmd = sys.executable + f" ./{moduleName}.py" + args
    os.system(cmd)
    os.chdir(r"..")

# 用户输入
def choose():
    choice = input(Colors.RED + "DShell> " + Colors.END)
    if choice[:3] == "gen":
        executeModule(choice, "gen", "genScript")
    elif choice[:6] == "listen":
        executeModule(choice, "listen", "listening")
    elif choice[:4] == "tool":
        try:
            moduleName = toolDicData[choice.split()[1]]
            executeModule(choice, "tool", moduleName)
        except:
            pass
    elif choice[:7] == "vulscan":
        try:
            moduleName = vulDicData[choice.split()[1]]
            executeModule(choice, "vulscan", moduleName)
        except:
            pass
    elif choice[:4] == "help":
        print(serverParseArgs())
    elif choice == "0" or choice == "q":
        print("\nBye~\n")
        exit(0)
    else:
        pass

if __name__ == "__main__":
    Logo().printLogo()
    print(serverParseArgs())
    while True:
        try:
            choose()
        except KeyboardInterrupt:
            print("\nBye~")
            exit(0)