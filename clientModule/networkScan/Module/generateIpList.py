#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Author  : Cr4y0n
# @Software: PyCharm
# @Time    : 2020/12/20 17:32

from Module.checkLegalIP import checkLegalIP

def generateIpList(dstIP):
    ipList = []
    if "/" in dstIP:
        # 192.168.1.1/24
        ipBase, mask = dstIP.split("/")[0], dstIP.split("/")[1]
        if mask == "24":
            for i in range(0, 256):
                ip = ipBase[:ipBase.rfind(".") + 1] + str(i)
                ipList.append(ip)
    elif "-" in dstIP:
        # 192.168.1.1-100
        ipBase, rangeMax = dstIP.split("-")[0], dstIP.split("-")[1]
        rangeMin = ipBase.split(".")[-1]
        for i in range(int(rangeMin), int(rangeMax) + 1):
            ip = ipBase[:ipBase.rfind(".") + 1] + str(i)
            ipList.append(ip)
    elif "," in dstIP:
        # 192.168.1.1,192.168.2.2,192.168.3.3
        ipList = dstIP.split(",")
    elif checkLegalIP(dstIP):
        ipList.append(dstIP)
    return ipList

# if __name__ == "__main__":
#     while True:
#         ip = input("ip: ")
#         print(generateIpList(ip))