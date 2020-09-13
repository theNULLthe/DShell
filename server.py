#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Author  : yyxzz
# @Software: PyCharm
# @Time    : 2020/8/16 8:13

import socket
from serverModule.logo import Logo
from misc.color import Colors
from serverModule.shell import Shell

def connect(host, port):
    serverHost = host
    serverPort = port
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((serverHost, serverPort))
    server.listen(5)
    msg = "Server is Listening <%s:%s>" % (serverHost, serverPort)
    print(Colors.CYAN + msg + Colors.END)
    clientSocket, clientAddress = server.accept()
    msg = "[+] Receive The Connection <%s:%s>" % (clientAddress[0], clientAddress[1])
    print(Colors.GREEN + msg + Colors.END)
    return clientSocket, clientAddress

if __name__ == "__main__":
    # host = input("Input LHOST：")
    # port = int(input("Input LPORT："))
    Logo().printLogo()
    sendBufferSize = 4096
    recvBufferSize = 8192
    host = "127.0.0.1"
    port = 9999
    while True:
        clientSocket, clientAddress = connect(host, port)
        shell = Shell(clientSocket)
        while True:
            if not shell.shell():
                break
        clientSocket.shutdown(2)
        clientSocket.close()