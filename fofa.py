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
    ASN_RULE = 'p[4]/a/text()'
    ORG_RULE = 'p[5]/a/text()'
    PORT_RULE = '//a[@class="hsxa-port"]/text()'

    def __init__(self):
        self.bypass = None
        self.headers_use = ""
        self.level = 0
        self.host_set = set()
        self.timestamp_list = [set()]

        self.city_list = [set()]
        self.asn_list = [set()]
        self.org_list = [set()]
        self.port_list = [set()]
        self.oldLength = -1
        self.endcount = 0
        self.filename = ""
        self.countryList = []
        self.timestampIndex = 0
        # Fofa-hack 版本号
        self.VERSION_NUM = "2.1.12"
        # 登录最大重试次数
        self.MAX_LOGIN_RETRY_NUM = 3
        # 页面URL获取最大重试次数
        self.MAX_MATCH_RETRY_NUM = 3

        print('''
         ____  ____  ____  ____      
        | ===|/ () \| ===|/ () \     
        |__|  \____/|__| /__/\__\    
             _   _   ____   ____  __  __ 
            | |_| | / () \ / (__`|  |/  /
            |_| |_|/__/\__\\\\____)|__|\__\\ V{}

            公众号: 黑糖安全
        '''.format(self.VERSION_NUM))

    def logoutInitMsg(self):
        print(f'''[*] LEVEL = {self.level} , 初始化成功
[*] 爬取延时: {self.timeSleep}s
[*] 爬取关键字: {self.searchKey}
[*] 爬取结束数量: {self.endcount}
 [*] 输出格式为: {self.output}
[*] 存储文件名: {self.filename}
[*] 是否开启关键字fuzz: {self.fuzz}
[*] 是否开启代理: {self.isProxy}
'''
              )
        return

    def setProxy(self, proxy):
        """
        设置代理
        """
        proxies = {}
        if proxy:
            proxies = {
                'http': 'http://' + proxy,
                'https': 'http://' + proxy
            }
            self.isProxy = True
            return proxies
        else:
            self.isProxy = False
            return proxies

    def initKeyWord(self, keyword):
        tempkey = keyword.replace("'", '"')
        # print(tempkey)

        if '"' not in tempkey and ' ' not in tempkey:
            if "=" in tempkey:
                # print("=".join(tempkey.split("=")[1:]))
                tempkey = tempkey.split("=")[0] + '="' + "=".join(tempkey.split("=")[1:]) + '"'
            else:
                tempkey = '"{}"'.format(tempkey)
        return tempkey

    def init(self):
        parser = argparse.ArgumentParser(description='Fofa-hack v{} 使用说明'.format(self.VERSION_NUM))
        parser.add_argument('--timesleep', '-t', help='爬取每一页等待秒数,防止IP被Ban,默认为3', default=3)
        parser.add_argument('--timeout', '-to', help='爬取每一页的超时时间', default=10)
        parser.add_argument('--keyword', '-k', help='fofa搜索关键字,默认为test', required=True)
        parser.add_argument('--endcount', '-e', help='爬取结束数量')
        parser.add_argument('--level', '-l', help='爬取等级: 1-3 ,数字越大内容越详细,默认为 1')
        parser.add_argument('--output', '-o', help='输出格式:txt、json,默认为txt')
        parser.add_argument('--fuzz', '-f', help='关键字fuzz参数,增加内容获取粒度', action='store_true')
        parser.add_argument('--proxy', help="指定代理，代理格式 --proxy '127.0.0.1:7890'")
        args = parser.parse_args()
        self.timeSleep = int(args.timesleep)
        self.timeout = int(args.timeout)
        print("input: " + args.keyword)
        self.searchKey = self.initKeyWord(args.keyword)
        if args.endcount:
            self.endcount = int(args.endcount)
        else:
            self.endcount = 100
        self.level = args.level if args.level else "1"
        self.levelData = LevelData(self.level)
        self.fuzz = args.fuzz
        self.output = args.output if args.output else "txt"
        self.filename = "{}_{}.{}".format(unit.md5(self.searchKey), int(time.time()), self.output)
        self.outputData = OutputData(self.filename, self.level, pattern=self.output)
        self.proxy = self.setProxy(args.proxy)
        self.logoutInitMsg()

    def get_count_num(self, search_key):
        """
        获取关键字的搜索数量值
        :param search_key:
        :return:
        """
        searchbs64 = base64.b64encode(f'{search_key}'.encode()).decode()
        print("[*] 爬取页面为:https://fofa.info/result?qbase64=" + searchbs64)
        html = requests.get(url="https://fofa.info/result?qbase64=" + searchbs64,
                            headers=fofa_useragent.getFofaPageNumHeaders(), timeout=self.timeout,proxies=self.proxy).text
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

    def bypassAsn(self, context, index):
        tree = etree.HTML(context)
        leftList = tree.xpath(self.LEFT_LIST_RULE)
        asnList = list()
        for i in range(len(leftList)):
            if len(leftList[i].xpath(self.ASN_RULE)) > 0:
                asnData = leftList[i].xpath(self.ASN_RULE)[0].strip()
                # city = self.filterKeyword(cityURL, "country")
                if asnData not in self.asn_list[index] and asnData != None:
                    self.asn_list[index].add(asnData)
                    asnList.append(asnData)
        print(asnList)

        return asnList

    def bypassOrg(self, context, index):
        tree = etree.HTML(context)
        leftList = tree.xpath(self.LEFT_LIST_RULE)
        orgList = list()
        for i in range(len(leftList)):
            if len(leftList[i].xpath(self.ORG_RULE)) > 0:
                orgData = leftList[i].xpath(self.ORG_RULE)[0].strip()
                # city = self.filterKeyword(cityURL, "country")
                if orgData not in self.org_list[index] and orgData != None:
                    self.org_list[index].add(orgData)
                    orgList.append(orgData)
        print(orgList)
        return orgList

    def bypassCountry(self, context, index):
        tree = etree.HTML(context)
        leftList = tree.xpath(self.LEFT_LIST_RULE)
        countryList = list()
        for i in range(len(leftList)):
            if len(leftList[i].xpath(self.CITY_RULE)) > 0:
                cityURL = leftList[i].xpath(self.CITY_RULE)[0].strip()
                city = self.filterKeyword(cityURL, "country")
                if city not in self.city_list[index] and city != None:
                    self.city_list[index].add(city)
                    countryList.append(city)
        print(countryList)
        return countryList

    def bypassPort(self, context, index):
        tree = etree.HTML(context)
        dataList = tree.xpath(self.PORT_RULE)
        portList = list()
        for port in dataList:
            port = port.strip()
            if port not in self.port_list[index] and port != None:
                # print(self.PORT_SET)
                self.port_list[index].add(port)
                portList.append(port)
        print(portList)
        return portList

    def filterKeyword(self, keyURL, key):
        # print(keyURL)
        if "qbase64=" in keyURL:
            searchbs64 = keyURL.split("qbase64=")[1]
            search_key = base64.b64decode(searchbs64).decode()
            if key in search_key:
                pattern = r'{}="([^"]+)"'.format(key)
                match = re.search(pattern, search_key)
                city = match.group(1)
                return city
        return None

    def setIndexTimestamp(self, searchbs64, timestampIndex):
        try:
            request_url = 'https://fofa.info/result?qbase64=' + searchbs64 + "&full=false&page_size=10"
            # print(f'request_url:{request_url}')
            rep = requests.get(request_url, headers=fofa_useragent.getFofaPageNumHeaders(), timeout=self.timeout,proxies=self.proxy)
            # print(rep.text)
            timelist = self.getTimeList(rep.text)
            # print(timelist)
            for temptime in timelist:
                self.timestamp_list[timestampIndex].add(temptime)
            return rep
        except Exception as e:
            print(e)
            pass
        return None

    def fofa_spider_page(self, search_key, searchbs64, timestampIndex):
        """
        获取一页的数据
        :rtype: object
        """
        searchbs64 = searchbs64.replace("%3D", "=")
        # init_search_key = base64.b64decode(searchbs64).decode()
        init_search_key = search_key
        print("now search key: " + init_search_key)
        TEMP_RETRY_NUM = 0

        while TEMP_RETRY_NUM < self.MAX_MATCH_RETRY_NUM:
            try:
                rep = self.setIndexTimestamp(searchbs64, timestampIndex)
                self.saveData(rep)
                for url in self.levelData.formatData:
                    self.host_set.add(url)

                time.sleep(self.timeSleep)

                return rep.text

            except Exception as e:
                print("[-] error:{}".format(e))
                TEMP_RETRY_NUM += 1
                print('[-] 第{}次尝试获取页面URL'.format(TEMP_RETRY_NUM))
                pass

        print('[-] FOFA资源获取重试超过最大次数,程序退出')
        exit(0)

    def saveData(self, rep):
        """
        数据保存至文件
        @param rep:
        """
        self.levelData.startSpider(rep)
        # tree = etree.HTML(rep.text)
        # urllist = tree.xpath('//span[@class="hsxa-host"]/a/@href')
        print("[*] 已爬取条数 [{}]: ".format(len(self.host_set)) + str(self.levelData.formatData))

        self.outputData.output(self.levelData.formatData)
        # for i in self.levelData.formatData:
        #     with open(self.filename, 'a+', encoding="utf-8") as f:
        #         f.write(str(i) + "\n")

    def checkDataIsUpdate(self):
        """
        检测数据是否新增
            新增为 true
            未新增为 false
        @return:
        """
        return self.oldLength != len(self.host_set)

    def fofa_common_spider(self, search_key, searchbs64, index):
        # while len(self.host_set) < self.endcount and self.oldLength !=len(self.host_set):

        self.oldLength = len(self.host_set)
        self.timestamp_list[index].clear()
        context = self.fofa_spider_page(search_key, searchbs64, index)

        if len(self.host_set) >= self.endcount:
            print("[*] 在{}节点,数据爬取结束".format(index))
            finalint = self.remove_duplicate()
            print('[*] 去重结束，最终数据 ' + str(finalint) + ' 条\n')
            exit(0)
        if self.oldLength == len(self.host_set):
            print("[-] {}节点数据无新增,该节点枯萎".format(index))
            return

        if self.fuzz:
            self.fofa_fuzz_spider(search_key, context, index)

        search_key_modify = self.modify_search_time_url(search_key, index)
        # print(search_key_modify)
        searchbs64_modify = quote_plus(base64.b64encode(search_key_modify.encode()))
        # search_key = search_key_modify
        # searchbs64 = searchbs64_modify
        self.fofa_common_spider(search_key_modify, searchbs64_modify, index)

    def checkHostPort(self):
        """
        检测输入关键字是否包含了port,目前看来有两种情况：
            1、"116.63.67.65:8009"
            2、host="116.63.67.65:8009"
        @return:
        """
        if " " not in self.searchKey:
            if ":" in self.searchKey:
                return False
        if "host" in self.searchKey:
            result = re.findall('host="(.*?)"', self.searchKey)
            if len(result) > 0 and ":" in result:
                return False
        return True

        # search_key_modify= self.modify_search_time_url(search_key,index)
        # print(search_key_modify)
        # searchbs64_modify = quote_plus(base64.b64encode(search_key_modify.encode()))
        # search_key = search_key_modify
        # searchbs64 = searchbs64_modify

    def fuzzListAdd(self):
        self.timestampIndex += 1
        self.timestamp_list.append(set())
        self.city_list.append(set())
        self.asn_list.append(set())
        self.org_list.append(set())
        self.port_list.append(set())

    def fofa_fuzz_spider(self, search_key, context, index):
        """
        递归调用 fofa_common_spider 方法不断 fuzz
        @param search_key:
        @param searchbs64:
        @return:
        """

        '''
            fuzz部分
        '''
        FUZZ_LIST = ["country", "org", "asn", "port"]
        for fuzzKey in FUZZ_LIST:
            if fuzzKey not in search_key:
                if fuzzKey == "country":
                    dataList = self.bypassCountry(context, index)
                elif fuzzKey == "org":
                    dataList = self.bypassOrg(context, index)
                elif fuzzKey == "asn":
                    dataList = self.bypassAsn(context, index)
                elif fuzzKey == "port" and self.checkHostPort():
                    dataList = self.bypassPort(context, index)
                else:
                    dataList = []
                # countryList = self.bypassCountry(context, index)
                for data in dataList:
                    new_key = search_key + ' && {}="{}"'.format(fuzzKey, data)
                    # print("new_key: "+new_key)
                    searchbs64_modify = quote_plus(base64.b64encode(new_key.encode("utf-8")))
                    self.fuzzListAdd()
                    self.setIndexTimestamp(searchbs64_modify, self.timestampIndex)
                    # self.fofa_spider_page(search_key,searchbs64_modify,self.timestampIndex)
                    self.fofa_common_spider(new_key, searchbs64_modify, self.timestampIndex)

                for data in dataList:
                    new_key = search_key + ' && {}!="{}"'.format(fuzzKey, data)
                    # print("new_key: "+new_key)
                    searchbs64_modify = quote_plus(base64.b64encode(new_key.encode("utf-8")))
                    self.fuzzListAdd()
                    self.setIndexTimestamp(searchbs64_modify, self.timestampIndex)
                    # self.fofa_spider_page(search_key,searchbs64_modify,self.timestampIndex)
                    self.fofa_common_spider(new_key, searchbs64_modify, self.timestampIndex)

        # if "country" not in search_key:
        #     countryList = self.bypassCountry(context, index)
        #     for country in countryList:
        #         new_key = search_key + ' && country="' + str(country) + '"'
        #
        #         # print("new_key: "+new_key)
        #         searchbs64_modify = quote_plus(base64.b64encode(new_key.encode("utf-8")))
        #         self.fuzzListAdd()
        #         self.setIndexTimestamp(searchbs64_modify, self.timestampIndex)
        #         # self.fofa_spider_page(search_key,searchbs64_modify,self.timestampIndex)
        #         self.fofa_common_spider(new_key, searchbs64_modify, self.timestampIndex)
        # if "org" not in search_key:
        #     orgList = self.bypassOrg(context, index)
        #     for org in orgList:
        #         new_key = search_key + ' && org="' + str(org) + '"'
        #         # print(search_key)
        #         searchbs64_modify = quote_plus(base64.b64encode(new_key.encode("utf-8")))
        #         self.fuzzListAdd()
        #         self.setIndexTimestamp(searchbs64_modify, self.timestampIndex)
        #         # self.fofa_spider_page(search_key,searchbs64_modify,self.timestampIndex)
        #         self.fofa_common_spider(new_key, searchbs64_modify, self.timestampIndex)
        # if "asn" not in search_key:
        #     asnList = self.bypassAsn(context, index)
        #     for asn in asnList:
        #         new_key = search_key + ' && asn="' + str(asn) + '"'
        #         # print(search_key)
        #         searchbs64_modify = quote_plus(base64.b64encode(new_key.encode("utf-8")))
        #         self.fuzzListAdd()
        #         self.setIndexTimestamp(searchbs64_modify, self.timestampIndex)
        #         # self.fofa_spider_page(search_key,searchbs64_modify,self.timestampIndex)
        #         self.fofa_common_spider(new_key, searchbs64_modify, self.timestampIndex)
        # if "port" not in search_key and self.checkHostPort():
        #     portList = self.bypassPort(context, index)
        #     for port in portList:
        #         new_key = search_key + ' && port="' + str(port) + '"'
        #         # print(search_key)
        #         searchbs64_modify = quote_plus(base64.b64encode(new_key.encode("utf-8")))
        #         self.fuzzListAdd()
        #         self.setIndexTimestamp(searchbs64_modify, self.timestampIndex)
        #         # self.fofa_spider_page(search_key,searchbs64_modify,self.timestampIndex)
        #         self.fofa_common_spider(new_key, searchbs64_modify, self.timestampIndex)

    def modify_search_time_url(self, search_key, index):
        """
        根据时间修订搜索值
        :param search_key:
        :return:
        """

        # get before_time in search_key.
        # if there is no before_time, set tomorrow_time as default
        before_time_in_search_key = (datetime.today() + timedelta(days=1)).strftime('%Y-%m-%d')
        if "before=" in search_key:
            pattern = r'before="([^"]+)"'
            match = re.search(pattern, search_key)
            before_time_in_search_key = match.group(1)
        time_before_time_in_search_key = datetime.strptime(before_time_in_search_key, "%Y-%m-%d").date()
        # print(self.timestamp_list)
        # print(index)
        # print("self.timestamp_list :"+str(self.timestamp_list))
        # print("index: "+str(index)+" ; self.timestamp_list[index]: "+str(self.timestamp_list[index]))
        # regard the_earliest_time.tomorrow as optimized time_before
        timestamp_list = list(self.timestamp_list[index])
        timestamp_list.sort()
        # print(timestamp_list)

        time_first = timestamp_list[0].split(' ')[0].strip('\n').strip()
        time_first_time = datetime.strptime(time_first, "%Y-%m-%d").date()
        time_before = time_first_time + timedelta(days=1)

        # check if optimized time_before can be used
        if time_before >= time_before_time_in_search_key:
            time_before = time_before_time_in_search_key - timedelta(days=1)

        # print(time_before)

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

    def remove_duplicate(self):
        f = open(self.filename, "r", encoding='utf-8')
        text_list = []
        s = set()
        document = f.readlines()
        document_num = int(len(document))
        content = [x.strip() for x in document]
        for x in range(0, len(content)):
            text = content[x]
            if text not in s:
                s.add(text)
                text_list.append(text)
        with open("final_" + str(self.filename), 'a+', encoding='utf-8') as final:
            for i in range(len(text_list)):
                # s = str(i).split()
                s = str(text_list[i])
                s = s + '\n'
                final.write(s)
        f.close()
        final.close()
        return int(len(text_list))

    def main(self):
        self.init()
        print('[*] 开始运行')
        searchbs64 = self.get_count_num(self.searchKey)
        self.fofa_common_spider(self.searchKey, searchbs64, 0)

        print('[*] 抓取结束，共抓取数据 ' + str(len(self.host_set)) + ' 条\n')


if __name__ == '__main__':
    fofa = Fofa()
    fofa.main()