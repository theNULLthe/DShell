#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Author  : Cr4y0n
# @Software: PyCharm
# @Time    : 2021/2/24 17:27

import os
import zipfile
from argparse import ArgumentParser

class zipBurp():
    def __init__(self):
        self.banner()
        self.args = self.parseArgs()
        self.zipFile = self.args.file
        self.pwdFile = self.args.password
        for pwd in self.loadPassword(self.pwdFile):
            self.burp((self.zipFile, pwd))

    def banner(self):
        logo = """
         _      ______                  
        (_)     | ___ \                 
     _____ _ __ | |_/ /_   _ _ __ _ __  
    |_  / | '_ \| ___ \ | | | '__| '_ \ 
     / /| | |_) | |_/ / |_| | |  | |_) |
    /___|_| .__/\____/ \__,_|_|  | .__/ 
          | |                    | |    
          |_|                    |_|    

        Author: Cr4y0n
        Version: V1.0
          """
        print("\033[91m" + logo + "\033[0m")

    def burp(self, item):
        (zipFile, password) = item
        zFile = zipfile.ZipFile(zipFile, "r")
        try:
            zFile.extractall(path="./", pwd=password.encode())
        except RuntimeError:
            print("\r[test] : " + password, end="", flush=True)
            pass
        except:
            print("\nSomething Error:", password)
            pass
        else:
            print("\n[\033[92mSuccessfully\033[0m] : " + password)
            while True:
                choice = input("Continue or Stop ? [c/S] # ")
                if choice in ["c", "C"]:
                    return 0
                elif choice in ["", "s", "S"]:
                    os._exit(0)
                else:
                    continue

    def loadPassword(self, pwdFile):
        pwdList = []
        with open(pwdFile, "r") as f:
            for line in f:
                line = line.strip("\n")
                pwdList.append(line)
        return pwdList

    def parseArgs(self):
        parser = ArgumentParser()
        parser.add_argument('-f', '--file', required=True, help='zip file')
        parser.add_argument('-p', '--password', required=True, help='password file')
        return parser.parse_args()