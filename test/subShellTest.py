#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Author  : yyxzz
# @Software: PyCharm
# @Time    : 2020/8/17 0:00

import os
import chardet
import subprocess
from misc.encoding import Encode

recvBufferSize = 8192

def execCommand():
    while True:
        pwd = os.getcwd()
        currentUser = subprocess.run("whoami", shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, encoding=Encode.encoding).stdout.strip(r"\n").strip()
        title = "(%s) %s > " % (currentUser, pwd)
        cmd = input(title)
        if cmd == "exit" or cmd == "quit":
            return
        try:
            if cmd[:2] == "cd":
                os.chdir(cmd[3:])
            elif cmd[1] == ":":
                os.chdir(cmd)
            elif cmd[:4] == "type":
                result = subprocess.run(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                fileEncoding = chardet.detect(result.stdout)["encoding"]
                print(fileEncoding)
                print(result.stdout.decode(fileEncoding))
            else:
                result = subprocess.run(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                print(chardet.detect(result.stdout))
                print(type(result.stdout.decode(Encode.encoding))), "---------", len(result.stdout.decode(Encode.encoding))
                if result.returncode == 0:
                    print(result.stdout.decode(Encode.encoding)) if len(result.stdout.decode(Encode.encoding)) != 0 else print(cmd)
                else:
                    print(result.stderr.decode(Encode.encoding))
        except FileNotFoundError:
            print("No Such File or Directory！")
        except UnicodeDecodeError:
            print("Encode ERROR！")
        except:
            print("An ERROR !")

execCommand()
