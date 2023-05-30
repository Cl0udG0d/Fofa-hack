#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/9/14 22:20
# @Author  : Cl0udG0d
# @File    : fofa.py
# @Github: https://github.com/Cl0udG0d
import argparse
import time

from core.fofaC import FofaC
from tookit import unit, config
from tookit.levelData import LevelData
from tookit.outputData import OutputData
from tookit.unit import clipKeyWord, setProxy, outputLogo


def main():
    outputLogo()
    parser = argparse.ArgumentParser(description='Fofa-hack v{} 使用说明'.format(config.VERSION_NUM))
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--keyword', '-k', help='fofa搜索关键字')
    group.add_argument('--inputfile', '-i', help="指定文件,从文件中批量读取fofa语法")

    parser.add_argument('--timesleep', '-t', help='爬取每一页等待秒数,防止IP被Ban,默认为3', default=3)
    parser.add_argument('--timeout', '-to', help='爬取每一页的超时时间', default=10)
    parser.add_argument('--endcount', '-e', help='爬取结束数量')
    parser.add_argument('--level', '-l', help='爬取等级: 1-3 ,数字越大内容越详细,默认为 1')
    parser.add_argument('--output', '-o', help='输出格式:txt、json,默认为txt')
    parser.add_argument('--fuzz', '-f', help='关键字fuzz参数,增加内容获取粒度', action='store_true')
    parser.add_argument('--proxy', help="指定代理，代理格式 --proxy '127.0.0.1:7890'")
    args = parser.parse_args()

    time_sleep = int(args.timesleep)
    timeout = int(args.timeout)
    search_key = clipKeyWord(args.keyword) if args.keyword else None
    endcount = int(args.endcount) if args.endcount else 100
    level = args.level if args.level else "1"
    level_data = LevelData(level)
    fuzz = args.fuzz
    output = args.output if args.output else "txt"
    if search_key:
        filename = "{}_{}.{}".format(unit.md5(search_key), int(time.time()), output)
        output_data = OutputData(filename, level, pattern=output)
    else:
        filename = "暂无"
        output_data=None
    is_proxy, proxy = setProxy(args.proxy)
    inputfile = args.inputfile if args.inputfile else None
    fofa=FofaC(search_key,inputfile,filename,time_sleep,endcount,level,level_data,output,output_data,fuzz,timeout,is_proxy, proxy)
    fofa.start()


if __name__ == '__main__':
    main()