#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Author  : yyxzz
# @Software: PyCharm
# @Time    : 2020/8/15 17:17

import socket
from clentModule.shell import Shell

if __name__ == "__main__":
    # host = "127.0.0.1"
    # port = 9999
    # host = input("HOST：")
    # port = int(input("PORT："))
    host = "127.0.0.1"
    port = 9999
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(host, port)
    client.connect((host, port))
    shellObject = Shell(client)
    while True:
        if not shellObject.shell():
            break
    client.shutdown(2)
    client.close()
