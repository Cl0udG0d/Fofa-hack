#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/9/14 22:20
# @Author  : Cl0udG0d
# @File    : fofa.py
# @Github: https://github.com/Cl0udG0d
import argparse
import os
import sys
import time
from core.fofaMain import FofaMain
from tookit import unit, config
from tookit.levelData import LevelData
from tookit.outputData import OutputData
from tookit.unit import clipKeyWord, setProxy, outputLogo
import gettext
import locale
import base64

config.ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
if getattr(sys, 'frozen', None):
    dir = sys._MEIPASS
else:
    dir = config.ROOT_PATH
# 获取当前的语言设置
lang, _ = locale.getdefaultlocale()
if lang and lang.startswith('zh'):
    # 如果是中文环境，不需要翻译，直接用原始字符串
    _ = lambda x: x
else:
    # 如果是其他语言环境，则加载对应的翻译文件
    language = gettext.translation('fofa_hack', localedir=os.path.join(dir, "locale"), languages=['en'])
    language.install()
    _ = language.gettext


def main():
    outputLogo()
    parser = argparse.ArgumentParser(description=_("Fofa-hack v{} 使用说明").format(config.VERSION_NUM))
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--keyword', '-k', help=_('fofa搜索关键字'))
    group.add_argument('--inputfile', '-i', help=_("指定文件,从文件中批量读取fofa语法"))
    group.add_argument('--base', '-b', help=_("以base64的形式输入关键字 -b InRoaW5rcGhwIg=="))

    parser.add_argument('--timesleep', '-t', help=_('爬取每一页等待秒数,防止IP被Ban,默认为3'), default=3)
    parser.add_argument('--timeout', '-to', help=_('爬取每一页的超时时间,默认为180秒'), default=180)
    parser.add_argument('--endcount', '-e', help=_('爬取结束数量'))
    parser.add_argument('--level', '-l', help=_('爬取等级: 1-3 ,数字越大内容越详细,默认为 1'))
    parser.add_argument('--output', '-o', help=_('输出格式:txt、json,默认为txt'))
    parser.add_argument('--outputname','-on', help=_("指定输出文件名，默认文件名为 fofaHack"))
    parser.add_argument('--fuzz', '-f', help=_('关键字fuzz参数,增加内容获取粒度'), action='store_true')
    parser.add_argument('--proxy', help=_("指定代理，代理格式 --proxy '127.0.0.1:7890'"))

    # parser.add_argument('--type', type=str, choices=["common", "selenium"], default="common",
    #                     help="运行类型,默认为普通方式")
    args = parser.parse_args()

    time_sleep = int(args.timesleep)
    timeout = int(args.timeout)
    if args.keyword:
        search_key = clipKeyWord(args.keyword)
    else:
        base = args.base if args.base else None
        if base:
            try:
                search_key = base64.b64decode(base).decode('utf-8')
            except Exception as e:
                print(e)
                search_key = ""
                pass
        else:
            search_key = ""

    endcount = int(args.endcount) if args.endcount else 100
    level = args.level if args.level else "1"
    level_data = LevelData(level)
    fuzz = args.fuzz
    output = args.output if args.output else "txt"
    outputname = args.outputname if args.outputname else "fofaHack"

    if search_key:
        if outputname:
            filename="{}.{}".format(outputname,output)
            # 检查文件是否存在
            if os.path.exists(filename):
                # 如果存在，删除文件
                os.remove(filename)
                os.remove("final_"+filename)
        else:
            filename = "{}_{}.{}".format(unit.md5(search_key), int(time.time()), output)
        output_data = OutputData(filename, level, pattern=output)
    else:
        filename = _("暂无")
        output_data = None
    is_proxy, proxy = setProxy(args.proxy)
    # type = args.type
    inputfile = args.inputfile if args.inputfile else None
    if not inputfile and not search_key:
        print(_("未输入搜索内容"))
        exit(0)

    fofa = FofaMain(search_key, inputfile, filename, time_sleep, endcount, level, level_data, output, output_data,
                    fuzz, timeout, is_proxy, proxy)
    fofa.start()


if __name__ == '__main__':
    main()
