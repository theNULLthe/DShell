#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Author   : Cr4y0n
# @Software : PyCharm
# @Time     : 2021/05/20
# @Github   : https://github.com/Cr4y0nXX

# 密钥流生成密钥
def createKey(parameter, initialKey, keyLength):
    tmpKeyList = [] # 临时密钥序列（所有组合）
    cycleKeyList = []   # 周期密钥序列（末尾元素）
    resultKeyList = []  # 最终密钥序列（指定长度）
    parameterList = list(map(lambda x: int(x) - 1, list(parameter.split(" ")))) # 用于异或操作的位置
    tmpKeyList.append(list(map(lambda x: int(x), initialKey)))
    count = 0
    while True:
        # 存储每一轮的结果
        tmpList = [0 for i in range(len(initialKey))]
        tmpList[0] = tmpKeyList[count][int(parameterList[0])]
        # 依次异或
        for i in range(1, len(parameterList)):
            tmpList[0] ^= tmpKeyList[count][int(parameterList[i])]
        for i in range(1, len(initialKey)):
            tmpList[i] = tmpKeyList[count][i - 1]
        tmpKeyList.append(tmpList)
        count += 1
        if tmpKeyList[count] == tmpKeyList[0]:
            break
    for item in tmpKeyList[:-1]:
        cycleKeyList.append(item[-1])
    for i in range(keyLength):
        resultKeyList.append(cycleKeyList[i % len(cycleKeyList)])
    resultKeyList = [0, 1, 0, 1]
    return resultKeyList

# 字符串转二进制
def strToBin(massage):
    resultStr = ""
    for i in massage:
        tmp = bin(ord(i)).replace("0b", "")
        while len(tmp) < 8:
            tmp = "0" + tmp
        resultStr += tmp
    return resultStr

# 二进制转字符串
def binToStr(massage):
    resultStr = ""
    for i in range(0, len(massage), 8):
        tmp = int(massage[i:i + 8], 2)
        resultStr += chr(tmp)
    return resultStr

# 加解密
def encrypt_decrypt(binStr, keyList):
    resultStr = ""
    for i in range(len(binStr)):
        resultStr += str(int(list(binStr)[i]) ^ int(keyList[i % len(keyList)]))
    return resultStr

# 输入信息
def loadMassage():
    initialKey = "10010010"
    parameter = "1 6 8"
    keyLength = int(40)
    # 返回初始消息（明文 / 密文）、初始密钥、反馈参数、加密密钥长度
    return initialKey, parameter, keyLength

def encrypt(massage):
    initialKey, parameter, keyLength = loadMassage()
    binStr = strToBin(massage)
    # print("明文对应二进制序列：", binStr)
    keyList = createKey(parameter, initialKey, keyLength)
    cipherText_bin = encrypt_decrypt(binStr, keyList)
    # print("密文二进制：", cipherText_bin)
    cipherText_int2str = str(hex(int(cipherText_bin, 2))).replace("0x", "")
    return cipherText_int2str

def decrypt(massage):
    initialKey, parameter, keyLength = loadMassage()
    cipherText_bin = str(bin(int(massage, 16))).replace("0b", "")
    while len(cipherText_bin) % 4 != 0:
        cipherText_bin = "0" + cipherText_bin
    # print("密文二进制：", cipherText_bin)
    keyList = createKey(parameter, initialKey, keyLength)
    clearText_bin = encrypt_decrypt(cipherText_bin, keyList)
    clearText = binToStr(clearText_bin)
    return clearText

if __name__ == "__main__":
    while True:
        msg = input("> ")
        cipherText = encrypt(msg)
        print("密文：", cipherText)
        clearText = decrypt(cipherText)
        print("明文：", clearText)


