#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Author  : Cr4y0n
# @Software: PyCharm
# @Time    : 2020/12/15 20:41

# 全连接、SYN半连接、无状态

from scapy.all import *
from tqdm import tqdm
from socket import socket
from random import randrange
from Module.generateIpList import generateIpList
from Module.generatePortList import generatePortList
from multiprocessing import Pool, Manager, cpu_count

class Root():
    def __init__(self, dstIP, dstPort):
        self.dstIP = dstIP
        self.dstPort = dstPort
        self.pool = Pool()
        self.queue = Manager().Queue()
        self.dstPortList = generatePortList(self.dstPort)
        self.run()

    # 校验防火墙，发送ACK，返回RST则未过滤，其余过滤
    def existFireWall(self, dstPort):
        srcPort = randrange(1024, 65536)
        packet = IP(dst=self.dstIP) / TCP(sport=srcPort, dport=dstPort, flags="A")
        resp = sr1(packet, verbose=False, timeout=0.5)
        if resp is None:
            return True
        elif resp.haslayer("TCP"):
            if resp["TCP"].flags == "R":
                return False
            else:
                return True

    def outPut(self):
        outputList = []
        length = self.queue.qsize()
        for i in range(length):
            outputList.append(self.queue.get())
        outputList.sort()
        for i in outputList:
            # print("%d\t\tOpen"%(i))
            print(i)

    def run(self):
        pass

    def __getstate__(self):
        self_dict = self.__dict__.copy()
        del self_dict['pool']
        return self_dict

    def __setstate__(self, state):
        self.__dict__.update(state)


class TcpSynScan(Root):
    def sendPacket(self, dstPort):
        srcPort = randrange(1024, 65536)
        # if self.existFireWall(dstPort):
        #     self.queue.put((dstPort, "Filtered"))
        #     return
        ipLayer = IP(dst=self.dstIP)
        tcpLayer = TCP(sport=srcPort, dport=dstPort, flags="S")
        packet = ipLayer / tcpLayer
        resp = sr1(packet, verbose=False, timeout=1)
        if resp is None:
            pass
        elif resp.haslayer("TCP"):
            if resp["TCP"].flags == "SA":
                send(IP(dst=self.dstIP) / TCP(sport=srcPort, dport=dstPort, flags="AR"), verbose=False)
                self.queue.put((dstPort, "Open"))
            elif resp["TCP"].flags == "RA":
                pass
    def run(self):
        self.pool.map(self.sendPacket, self.dstPortList)
        self.pool.close()
        self.pool.join()
        self.pool.terminate()
        self.outPut()

class TcpFinScan(Root):
    def sendPacket(self, dstPort):
        srcPort = randrange(1024, 65536)
        ipLayer = IP(dst=self.dstIP)
        tcpLayer = TCP(sport=srcPort, dport=dstPort, flags="F")
        packet = ipLayer / tcpLayer
        print(packet.show())
        resp = sr1(packet, verbose=False, timeout=1)
        if resp is None:
            self.queue.put(dstPort)
        elif resp.haslayer("TCP"):
            print(resp.show())
            if resp["TCP"].flags == "R":
                pass
            else:
                pass
    def run(self):
        self.pool.map(self.sendPacket, self.dstPortList)
        self.pool.close()
        self.pool.join()
        self.pool.terminate()
        self.outPut()

class TcpNullScan(Root):
    def sendPacket(self, dstPort):
        srcPort = randrange(1024, 65536)
        ipLayer = IP(dst=self.dstIP)
        tcpLayer = TCP(sport=srcPort, dport=dstPort, flags="")
        packet = ipLayer / tcpLayer
        resp = sr1(packet, verbose=False, timeout=1)
        if resp is None:
            self.queue.put(dstPort)
        elif resp.haslayer("TCP"):
            if resp["TCP"].flags == "R":
                pass
            else:
                pass
    def run(self):
        self.pool.map(self.sendPacket, self.dstPortList)
        self.pool.close()
        self.pool.join()
        self.pool.terminate()
        self.outPut()

class TcpConnectScan(Root):
    def sendPacket(self, dstPort):
        try:
            conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            conn.connect((self.dstIP, dstPort))
            self.queue.put(dstPort)
            conn.close()
        except:
            pass
    def run(self):
        self.pool.map(self.sendPacket, self.dstPortList)
        self.pool.close()
        self.pool.join()
        self.pool.terminate()

if __name__ == "__main__":
    dstIP = "127.0.0.1"
    # dstIP = "139.155.35.193"
    dstPort = input("port: ")
    t1 = time.time()
    TcpSynScan(dstIP, dstPort)
    # TcpFinScan(dstIP, dstPort)
    # TcpNullScan(dstIP, dstPort)
    t2 = time.time()
    print("Finished In %.2f Sec"%(t2 - t1))

