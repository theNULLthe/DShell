#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Author  : Cr4y0n
# @Software: PyCharm
# @Time    : 2021/4/8 21:08

import sys
from argparse import ArgumentParser

# 监听模块参数
def listeningParseArgs():
    parser = ArgumentParser()
    parser.add_argument("-lh", "--lhost", type=str, required=False, default="0.0.0.0", help=f"The listening host, default is 0.0.0.0")
    parser.add_argument("-lp", "--lport", type=int, required=False, default=1116, help=f"The listening port, default is 1116")
    # parser.add_help()
    return parser.parse_args()

# 生成脚本模块参数
def genScriptParseArgs():
    # parser = ArgumentParser()
    parser = ArgumentParser(prog="gen")
    parser.add_argument("-lh", "--lhost", type=str, required=True, help=f"The listening host")
    parser.add_argument("-lp", "--lport", type=int, required=False, default=1116, help=f"The listening port, default is 1116")
    parser.add_argument("-a", "--platform", type=str, required=True, choices=["win", "linux"], help=f"The remote platform (win or linux)")
    parser.add_argument("--screenHost", action="store_true", default=False, help=f"open screen host script")
    return parser.parse_args()

if __name__ == "__main__":
    try:
        args = genScriptParseArgs()
    except Exception as e:
        print('str(Exception):\t', str(Exception))
    # print(sys.stderr())
    # print(args.accumulate(args.integers))