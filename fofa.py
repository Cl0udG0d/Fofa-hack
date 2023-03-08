#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/9/14 22:20
# @Author  : Cl0udG0d
# @File    : fofa.py
# @Github: https://github.com/Cl0udG0d
from datetime import datetime
from datetime import timedelta
import base64
import time
from urllib.parse import quote_plus
import config
from tookit import unit, fofa_useragent
import argparse
from tookit.levelData import LevelData
from tookit.outputData import OutputData
import re, requests
from lxml import etree



class Fofa:
    def __init__(self):
        self.headers_use = ""
        self.level = 0
        self.host_set = set()
        self.timestamp_set = set()
        self.oldLength = -1
        self.endcount=0
        self.filename = ""

        print('''
         ____  ____  ____  ____      
        | ===|/ () \| ===|/ () \     
        |__|  \____/|__| /__/\__\    
             _   _   ____   ____  __  __ 
            | |_| | / () \ / (__`|  |/  /
            |_| |_|/__/\__\\\\____)|__|\__\\ V{}
        '''.format(config.VERSION_NUM))

    def headers(self,cookie):
        headers_use = {
            'User-Agent': fofa_useragent.getFakeUserAgent(),
            'Accept': 'application/json, text/plain, */*',
            "cookie": cookie.encode("utf-8").decode("latin1")
        }
        return headers_use

    def logoutInitMsg(self):
        print('''[*] LEVEL = {} , 初始化成功
[*] 爬取延时: {}s
[*] 爬取关键字: {}
[*] 爬取结束数量: {}
[*] 是否FUZZ: {}
[*] 输出格式为: {}
[*] 存储文件名: {}'''.format(self.level,self.timeSleep,self.searchKey,self.endcount,self.fuzz,self.output,self.filename)
        )
        return

    def init(self):
        parser = argparse.ArgumentParser(description='Fofa-hack v{} 使用说明'.format(config.VERSION_NUM))
        parser.add_argument('--timesleep', '-t', help='爬取每一页等待秒数,防止IP被Ban,默认为3',default=3)
        parser.add_argument('--keyword', '-k', help='fofa搜索关键字,默认为test', required=True)
        parser.add_argument('--endcount', '-e', help='爬取结束数量')
        parser.add_argument('--level', '-l', help='爬取等级: 1-3 ,数字越大内容越详细,默认为 1')
        parser.add_argument('--output', '-o', help='输出格式:txt、json、csv,默认为txt')
        parser.add_argument('--fuzz', '-f', help='关键字fuzz参数,增加内容获取粒度',action='store_true')
        args = parser.parse_args()
        self.timeSleep= int(args.timesleep)
        self.searchKey= args.keyword
        if args.endcount:
            self.endcount=int(args.endcount)
        else:
            self.endcount=100
        self.level=args.level if args.level else "1"
        self.levelData=LevelData(self.level)
        self.fuzz=args.fuzz
        self.output = args.output if args.output else "txt"
        self.filename = "{}_{}.{}".format(unit.md5(self.searchKey), int(time.time()),self.output)
        self.outputData = OutputData(self.filename, pattern=self.output)
        self.logoutInitMsg()

    def get_count_num(self, search_key):
        """
        获取关键字的搜索数量值
        :param search_key:
        :return:
        """
        headers_use = fofa_useragent.getFofaPageNumHeaders()
        searchbs64 = base64.b64encode(f'{search_key}'.encode()).decode()
        print("[*] 爬取页面为:https://fofa.info/result?qbase64=" + searchbs64)
        html = requests.get(url="https://fofa.info/result?qbase64=" + searchbs64, headers=headers_use).text
        tree = etree.HTML(html)
        try:
            countnum = tree.xpath('//span[@class="hsxa-highlight-color"]/text()')[0]
            # standaloneIpNum = tree.xpath('//span[@class="hsxa-highlight-color"]/text()')[1]
        except Exception as e:
            print("[-] error:{}".format(e))
            countnum = '0'
            pass
        print("[*] 存在数量:" + countnum)
        # print("[*] 独立IP数量:" + standaloneIpNum)
        return searchbs64

    def getTimeList(self, text):
        """
        获取时间列表
        :param text:
        :return:
        """
        timelist = list()
        pattern = "<span>[0-9]*-[0-9]*-[0-9]*</span>"
        result = re.findall(pattern, text)
        for temp in result:
            timelist.append(temp.replace("<span>", "").replace("</span>", "").strip())
        return timelist

    def fofa_spider_page(self, searchbs64):
        """
        获取一页的数据
        :rtype: object
        """
        TEMP_RETRY_NUM=0

        while TEMP_RETRY_NUM < config.MAX_MATCH_RETRY_NUM:
            try:
                request_url = 'https://fofa.info/result?qbase64=' + searchbs64 + "&full=false&page_size=10"
                # print(f'request_url:{request_url}')
                rep = requests.get(request_url, headers=self.headers_use)
                self.levelData.startSpider(rep)

                # tree = etree.HTML(rep.text)
                # urllist = tree.xpath('//span[@class="hsxa-host"]/a/@href')
                timelist = self.getTimeList(rep.text)
                print("[*] 已爬取条数 [{}]: ".format(len(self.host_set))+str(self.levelData.formatData))

                for i in self.levelData.formatData:
                    with open(self.filename, 'a+', encoding="utf-8") as f:
                        f.write(str(i) + "\n")
                for url in self.levelData.formatData:
                    self.host_set.add(url)
                for temptime in timelist:
                    self.timestamp_set.add(temptime)
                time.sleep(self.timeSleep)
                return
            except Exception as e:
                print("[-] error:{}".format(e))
                TEMP_RETRY_NUM+=1
                print('[-] 第{}次尝试获取页面URL'.format(TEMP_RETRY_NUM))
                pass


        print('[-] FOFA资源获取重试超过最大次数,程序退出')
        exit(0)


    def fofa_common_spider(self, search_key, searchbs64):
        while len(self.host_set) < self.endcount and self.oldLength !=len(self.host_set):
            self.oldLength=len(self.host_set)
            self.timestamp_set.clear()
            self.fofa_spider_page(searchbs64)
            search_key_modify= self.modify_search_time_url(search_key)
            searchbs64_modify = quote_plus(base64.b64encode(search_key_modify.encode()))
            search_key = search_key_modify
            searchbs64 = searchbs64_modify
        if len(self.host_set) >= self.endcount:
            print("[*] 数据爬取结束")
            return
        if self.oldLength == len(self.host_set):
            print("[-] 数据无新增,退出爬取")
            return

    def fofa_fuzz_spider(self, search_key, searchbs64):
        while len(self.host_set) < self.endcount and self.oldLength !=len(self.host_set):
            self.oldLength=len(self.host_set)
            self.timestamp_set.clear()
            self.fofa_spider_page(searchbs64)
            search_key_modify = self.modify_search_time_url(search_key)

            searchbs64_modify = quote_plus(base64.b64encode(search_key_modify.encode()))
            search_key = search_key_modify
            searchbs64 = searchbs64_modify
        if len(self.host_set) >= self.endcount:
            print("[*] 数据爬取结束")
            return
        if self.oldLength == len(self.host_set):
            print("[-] 数据无新增,退出爬取")
            return

    def modify_search_time_url(self, search_key):
        """
        根据时间修订搜索值
        :param search_key:
        :return:
        """
        timestamp_list=list(self.timestamp_set)
        timestamp_list.sort()
        # timestamp_length = len(timestamp_list)
        if timestamp_list[-1] == timestamp_list[0]:
            time_before = timestamp_list[-1].strip('\n').strip()
        else:
            time_last = timestamp_list[-1].split(' ')[0].strip('\n').strip()
            # print(time_last)
            time_last_time = datetime.strptime(time_last, "%Y-%m-%d").date()
            # print(str(time_last_time))
            time_before = (time_last_time - timedelta(days=1))
            # print('time_before' + str(time_before))
        if 'before' in search_key:
            search_key = search_key.split('&& before')[0]
            search_key = search_key.strip(' ')
            search_key = search_key + ' && ' + 'before="' + str(time_before) + '"'
        else:
            search_key = search_key + ' && ' + 'before="' + str(time_before) + '"'
        search_key_modify = search_key


        # print('[*] 搜索词： ' + search_key_modify)

        return search_key_modify

    def run(self):
        searchbs64 = self.get_count_num(self.searchKey)
        if not self.fuzz:
            self.fofa_common_spider(self.searchKey, searchbs64)
        else:
            self.fofa_fuzz_spider(self.searchKey, searchbs64)
        print('[*] 抓取结束，共抓取数据 ' + str(len(self.host_set)) + ' 条\n')

    def main(self):
        self.init()
        print('[*] 开始运行')
        self.run()

if __name__ == '__main__':
    fofa = Fofa()
    fofa.main()
