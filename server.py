#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Author  : Cr4y0n
# @Software: PyCharm
# @Time    : 2021/4/8 23:42

import os
import sys
from misc.logo import Logo

# 根据关键字执行相应模块
def executeModule(choice, keyWord, moduleName):
    args = choice[len(keyWord):]
    os.chdir(r"./serverModule")
    cmd = sys.executable + f" ./{moduleName}.py" + args
    os.system(cmd)
    os.chdir(r"..")

# 用户输入
def choose():
    choice = input("DShell > ")
    if choice[:3] == "gen":
        executeModule(choice, "gen", "genScript")
    elif choice[:6] == "listen":
        executeModule(choice, "listen", "listening")
    elif choice == "3":
        print("Waiting……")
    elif choice == "4":
        print("Waiting……")
    elif choice[:10] == "urlExtract":
        args = choice[10:]
        cmd = sys.executable + " ./tools/urlExtractor.py" + args
        os.system(cmd)
    elif choice == "0" or choice == "q":
        print("\nBye~\n")
        os._exit(0)
    else:
        pass

if __name__ == "__main__":
    Logo().printLogo()
    # checkEnvironment()
    while True:
        try:
            choose()
        except KeyboardInterrupt:
            print("\nBye~")
            os._exit(0)