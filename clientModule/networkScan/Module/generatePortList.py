#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Author  : Cr4y0n
# @Software: PyCharm
# @Time    : 2020/12/20 17:35

def generatePortList(dstPort):
    portList = []
    if "-" in dstPort:
        # 1-100
        rangeMin, rangeMax = int(dstPort.split("-")[0]), int(dstPort.split("-")[1])
        if rangeMin >= 0 and rangeMax <= 65536 and rangeMin < rangeMax:
            for i in range(rangeMin, rangeMax + 1):
                portList.append(i)
    elif "," in dstPort:
        # 1,2,3,4,5,9
        portList = list(map(lambda x: int(x), dstPort.split(",")))
    elif dstPort.isdigit():
        # 3306
        if 0 <= int(dstPort) and 65536>= int(dstPort):
            portList.append(int(dstPort))
    return portList

# if __name__ == "__main__":
#     while True:
#         port = input("port: ")
#         print(generatePortList(port))