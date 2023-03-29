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

from tookit.bypass import ByPass
from tookit.levelData import LevelData
from tookit.outputData import OutputData
import re, requests
from lxml import etree



class Fofa:
    '''
    FUZZ规则
    '''
    LEFT_LIST_RULE = '//div[@class="hsxa-meta-data-list-main-left hsxa-fl"]'
    CITY_RULE = 'p[3]/a/@href'

    CITY_SET = set()


    def __init__(self):
        self.bypass = None
        self.headers_use = ""
        self.level = 0
        self.host_set = set()
        self.timestamp_list=[set()]
        self.oldLength = -1
        self.endcount=0
        self.filename = ""
        self.countryList=[]
        self.timestampIndex=0

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
[*] 输出格式为: {}
[*] 存储文件名: {}'''.format(self.level,self.timeSleep,self.searchKey,self.endcount,self.output,self.filename)
        )
        return

    def initKeyWord(self,keyword):
        tempkey=keyword.replace("'",'"')
        if '"' not in tempkey and ' ' not in tempkey:
            tempkey='"{}"'.format(tempkey)
        return tempkey

    def init(self):
        parser = argparse.ArgumentParser(description='Fofa-hack v{} 使用说明'.format(config.VERSION_NUM))
        parser.add_argument('--timesleep', '-t', help='爬取每一页等待秒数,防止IP被Ban,默认为3',default=3)
        parser.add_argument('--timeout', '-to', help='爬取每一页的超时时间',default=10)
        parser.add_argument('--keyword', '-k', help='fofa搜索关键字,默认为test', required=True)
        parser.add_argument('--endcount', '-e', help='爬取结束数量')
        parser.add_argument('--level', '-l', help='爬取等级: 1-3 ,数字越大内容越详细,默认为 1')
        parser.add_argument('--output', '-o', help='输出格式:txt、json,默认为txt')
        # parser.add_argument('--fuzz', '-f', help='关键字fuzz参数,增加内容获取粒度',action='store_true')
        args = parser.parse_args()
        self.timeSleep= int(args.timesleep)
        self.timeout = int(args.timeout)
        self.searchKey=self.initKeyWord(args.keyword)
        if args.endcount:
            self.endcount=int(args.endcount)
        else:
            self.endcount=100
        self.level=args.level if args.level else "1"
        self.levelData=LevelData(self.level)
        # self.fuzz=args.fuzz
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
        html = requests.get(url="https://fofa.info/result?qbase64=" + searchbs64, headers=headers_use, timeout=self.timeout).text
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

    def bypassCountry(self,context):
        tree = etree.HTML(context)
        leftList = tree.xpath(self.LEFT_LIST_RULE)
        countryList=list()
        for i in range(len(leftList)):
            if len(leftList[i].xpath(self.CITY_RULE))>0:
                cityURL = leftList[i].xpath(self.CITY_RULE)[0].strip()
                city=self.filterKeyword(cityURL,"country")
                if city not in self.CITY_SET and city!=None:
                    self.CITY_SET.add(city)
                    countryList.append(city)
        # print(countryList)
        return countryList

    def filterKeyword(self,keyURL,key):
        # print(keyURL)
        searchbs64=keyURL.split("qbase64=")[1]
        search_key=base64.b64decode(searchbs64).decode()
        if key in search_key:
            pattern = r'{}="([^"]+)"'.format(key)
            match = re.search(pattern, search_key)
            city = match.group(1)
            return city

    def fofa_spider_page(self, searchbs64,timestampIndex=0):
        """
        获取一页的数据
        :rtype: object
        """
        searchbs64=searchbs64.replace("%3D","=")
        init_search_key = base64.b64decode(searchbs64).decode()
        print(init_search_key)
        TEMP_RETRY_NUM=0

        while TEMP_RETRY_NUM < config.MAX_MATCH_RETRY_NUM:
            # try:
                request_url = 'https://fofa.info/result?qbase64=' + searchbs64 + "&full=false&page_size=10"
                # print(f'request_url:{request_url}')
                rep = requests.get(request_url, headers=self.headers_use, timeout=self.timeout)
                timelist = self.getTimeList(rep.text)
                # print(timelist)
                for temptime in timelist:
                    self.timestamp_list[self.timestampIndex].add(temptime)

                self.saveData(rep)
                for url in self.levelData.formatData:
                    self.host_set.add(url)

                time.sleep(self.timeSleep)
                '''
                fuzz部分
                '''
                # self.bypass = ByPass(rep.text)
                if "country" not in init_search_key:
                    countryList=self.bypassCountry(rep.text)
                    for country in countryList:
                        search_key = init_search_key+ ' && country="' + str(country) + '"'
                        # print(search_key)
                        searchbs64_modify = quote_plus(base64.b64encode(search_key.encode("utf-8")))
                        self.timestampIndex+=1
                        self.timestamp_list.append(set())
                        self.fofa_common_spider(search_key,searchbs64_modify,self.timestampIndex)
                return
            # except Exception as e:
            #     print("[-] error:{}".format(e))
            #     TEMP_RETRY_NUM+=1
            #     print('[-] 第{}次尝试获取页面URL'.format(TEMP_RETRY_NUM))
            #     pass


        print('[-] FOFA资源获取重试超过最大次数,程序退出')
        exit(0)

    def saveData(self,rep):
        """
        数据保存至文件
        @param rep:
        """
        self.levelData.startSpider(rep)
        # tree = etree.HTML(rep.text)
        # urllist = tree.xpath('//span[@class="hsxa-host"]/a/@href')
        print("[*] 已爬取条数 [{}]: ".format(len(self.host_set)) + str(self.levelData.formatData))

        for i in self.levelData.formatData:
            with open(self.filename, 'a+', encoding="utf-8") as f:
                f.write(str(i) + "\n")

    def fofa_common_spider(self, search_key, searchbs64,index):
        while len(self.host_set) < self.endcount and self.oldLength !=len(self.host_set):
            self.oldLength=len(self.host_set)
            self.timestamp_list[index].clear()
            self.fofa_spider_page(searchbs64)
            search_key_modify= self.modify_search_time_url(search_key,index)
            # print(search_key_modify)
            searchbs64_modify = quote_plus(base64.b64encode(search_key_modify.encode()))
            search_key = search_key_modify
            searchbs64 = searchbs64_modify
        if len(self.host_set) >= self.endcount:
            # print("[*] 在{}节点,数据爬取结束".format(index))
            return
        if self.oldLength == len(self.host_set):
            print("[-] {}节点数据无新增,该节点枯萎".format(index))
            return

    # def fofa_fuzz_spider(self, search_key, searchbs64):
    #     """
    #     递归调用 fofa_common_spider 方法不断 fuzz
    #     @param search_key:
    #     @param searchbs64:
    #     @return:
    #     """
    #     FUZZ_LIST=["country","port","server","protocol","title"]
    #     for key in FUZZ_LIST:
    #         if key not in search_key:
    #             results=self.bypass.switchBypass(key)
    #             for result in results:
    #                 search_key = search_key + ' && ' + key +'="' + str(result) + '"'
    #                 searchbs64_modify = quote_plus(base64.b64encode(search_key.encode()))
    #                 self.fofa_common_spider(search_key,searchbs64_modify)

    # def fuzzCountry(self):
    #     return

    def modify_search_time_url(self, search_key,index):
        """
        根据时间修订搜索值
        :param search_key:
        :return:
        """
        
        # get before_time in search_key.
        # if there is no before_time, set tomorrow_time as default
        before_time_in_search_key = (datetime.today()+timedelta(days=1)).strftime('%Y-%m-%d')
        if "before=" in search_key:
            pattern = r'before="([^"]+)"'
            match = re.search(pattern, search_key)
            before_time_in_search_key = match.group(1)
        time_before_time_in_search_key = datetime.strptime(before_time_in_search_key, "%Y-%m-%d").date()
        # print(self.timestamp_list)
        # print(index)
        # regard the_earliest_time.tomorrow as optimized time_before
        timestamp_list=list(self.timestamp_list[index])
        timestamp_list.sort()
        # print(timestamp_list)

        time_first = timestamp_list[0].split(' ')[0].strip('\n').strip()
        time_first_time = datetime.strptime(time_first, "%Y-%m-%d").date()
        time_before = time_first_time+timedelta(days=1)
        
        # check if optimized time_before can be used
        if time_before>=time_before_time_in_search_key:
            time_before = time_before_time_in_search_key - timedelta(days=1)
 
        #print(time_before)

        if 'before' in search_key:
            # print(search_key)
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
        self.fofa_common_spider(self.searchKey, searchbs64,0)

        print('[*] 抓取结束，共抓取数据 ' + str(len(self.host_set)) + ' 条\n')

    def main(self):
        self.init()
        print('[*] 开始运行')
        self.run()

if __name__ == '__main__':
    fofa = Fofa()
    fofa.main()
