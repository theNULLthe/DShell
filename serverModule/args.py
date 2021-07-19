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
    return parser.parse_args()

# 生成脚本模块参数
def genScriptParseArgs():
    parser = ArgumentParser(prog="gen")
    parser.add_argument("-lh", "--lhost", type=str, required=True, help=f"The listening host")
    parser.add_argument("-lp", "--lport", type=int, required=False, default=1116, help=f"The listening port, default is 1116")
    parser.add_argument("-a", "--platform", type=str, required=True, choices=["win", "linux"], help=f"The remote platform (win or linux)")
    parser.add_argument("--screenHost", action="store_true", default=False, help=f"open screen host script")
    return parser.parse_args()

# server文件参数
def serverParseArgs():
    args = """
Global Module
--------------------------------------------------------------------
    gen       [lhost]<lport>     Generate a acript
    listen    [lhost]<lport>     Create a listener
    vulscan   [pocName]<args>    Vulnerability scanning
    tool      [toolName]<args>   Use some tools


vulScan Module
--------------------------------------------------------------------
    ApacheSolrRAF                Apache Solr Read Any File POC
    ApacheSolrRAF_EXP            Apache Solr Read Any File EXP
    KyanInfoDisc                 Kyan information disclosure POC
    KyanInfoDisc_EXP             Kyan information disclosure EXP
    phpstudyRCE                  phpStudy Remote Command/Code EXEC POC
    phpstudyRCE_EXP              phpStudy Remote Command/Code EXEC EXP
    ShowDocUAF                   ShowDoc Upload Any File POC
    ShowDocUAF_EXP               ShowDoc Upload Any File EXP
    TerraMasterRAF               TerraMaster TOS Read Any File
    ZeroShellRCE                 ZeroShell Firewall Remote Command/Code EXEC
    LandrayRAF                   Landray OA Read Any File POC
    LandrayRAF_EXP               Landray OA Read Any File EXP
    LandrayRAF_EXP_passExport    Landray OA Read Any File EXP_passExport


Tools Module
--------------------------------------------------------------------
    urlExt    [urlExtractor]     Extract the URL from the project
    zipBurp   [zipBurp]          Burst a zip file
    siteScan  [file]             Discover the site on the IP address
    """
    return f"\033[34m{args}\033[0m"

if __name__ == "__main__":
    try:
        args = genScriptParseArgs()
    except Exception as e:
        print('str(Exception):\t', str(Exception))