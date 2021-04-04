#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Author  : Cr4y0n
# @Software: PyCharm
# @Time    : 2021/03/11

# def DShellSend(socket, data):
#     if type(data) == bytes:
#         dataByte = data
#     else:
#         dataByte = data.encode("gbk")
#     socket.sendall(("%s"%(len(dataByte))).encode("gbk"))
#     socket.sendall(dataByte)
#
# def DShellRecv(socket):
#     resultSize = socket.recv(1024).decode("gbk")
#     recvSize = 0
#     result = b""
#     while recvSize < int(resultSize):
#         result += socket.recv(1024)
#         recvSize = len(result)
#     return result.decode("gbk")

def DShellSend(socket, data):
    if type(data) == bytes:
        dataByte = data
    else:
        dataByte = data.encode("gbk")
    # socket.send((f"{len(dataByte): s}").encode("gbk"))
    socket.sendall(("%s"%(len(dataByte))).encode("gbk"))
    status = socket.recv(1024).decode("gbk")
    socket.sendall(dataByte)
    status = socket.recv(1024).decode("gbk")

def DShellRecv(socket):
    resultSize = socket.recv(1024).decode("gbk")
    socket.sendall("OK".encode("gbk"))
    recvSize = 0
    result = b""
    while recvSize < int(resultSize):
        result += socket.recv(1024)
        recvSize = len(result)
    # print(result.decode("gbk"))
    socket.sendall("OK".encode("gbk"))
    return result.decode("gbk")

if __name__ == "__main__":
    a = b"aaa"
    if type(a) == bytes:
        print("yes")


