#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Author  : Cr4y0n
# @Software: PyCharm
# @Time    : 2020/12/20 17:26

def checkLegalIP(ip):
    try:
        data = list(ip.split("."))
        if len(data) == 4:
            for i in data:
                if int(i) < 0 or int(i) > 255:
                    return False
            return True
        return False
    except:
        return False