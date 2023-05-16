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
        """
        初始化方法
        """
        self.bypass = None
        self.headers_use = ""
        self.level = 0
        self.host_set = set()
        self.timestamp_list = [set()]

        self.city_list = [set()]
        self.asn_list = [set()]
        self.org_list = [set()]
        self.port_list = [set()]
        self.old_length = -1
        self.endcount = 0
        self.filename = ""
        self.country_list = []
        self.timestamp_index = 0
        self.no_new_data_count = 0
        # Fofa-hack 版本号
        self.VERSION_NUM = "2.2.4"
        # 登录最大重试次数
        self.MAX_LOGIN_RETRY_NUM = 3
        # 页面URL获取最大重试次数
        self.MAX_MATCH_RETRY_NUM = 3
        self.EXIT_FLAG = False

        print('''
         ____  ____  ____  ____      
        | ===|/ () \| ===|/ () \     
        |__|  \____/|__| /__/\__\    
             _   _   ____   ____  __  __ 
            | |_| | / () \ / (__`|  |/  /
            |_| |_|/__/\__\\\\____)|__|\__\\ V{}

            公众号: 黑糖安全
        '''.format(self.VERSION_NUM))

    def outInitMsg(self):
        """
        输出初始化信息
        """
        print(f'''[*] LEVEL = {self.level} , 初始化成功
[*] 爬取延时: {self.time_sleep}s
[*] 爬取关键字: {self.search_key}
[*] 爬取结束数量: {self.endcount}
[*] 输出格式为: {self.output}
[*] 存储文件名: {self.filename}
[*] 是否开启关键字fuzz: {self.fuzz}
[*] 是否开启代理: {self.is_proxy}
''')

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
            self.is_proxy = True
            return proxies
        else:
            self.is_proxy = False
            return proxies

    def clipKeyWord(self, keyword):
        """
        修剪查找关键字
        @param keyword:
        @return:
        """
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
        self.time_sleep = int(args.timesleep)
        self.timeout = int(args.timeout)
        print("input: " + args.keyword)
        self.search_key = self.clipKeyWord(args.keyword)
        if args.endcount:
            self.endcount = int(args.endcount)
        else:
            self.endcount = 100
        self.level = args.level if args.level else "1"
        self.level_data = LevelData(self.level)
        self.fuzz = args.fuzz
        self.output = args.output if args.output else "txt"
        self.filename = "{}_{}.{}".format(unit.md5(self.search_key), int(time.time()), self.output)
        self.output_data = OutputData(self.filename, self.level, pattern=self.output)
        self.proxy = self.setProxy(args.proxy)
        self.outInitMsg()

    def getFofaKeywordsCount(self, search_key):
        """
        获取关键字的搜索数量值
        :param search_key:
        :return:
        """
        searchbs64 = base64.b64encode(f'{search_key}'.encode()).decode()
        print("[*] 爬取页面为:https://fofa.info/result?qbase64=" + searchbs64)
        html = requests.get(url="https://fofa.info/result?qbase64=" + searchbs64,
                            headers=fofa_useragent.getFofaPageNumHeaders(), timeout=self.timeout,proxies=self.proxy)\
                            .text
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
        """
        通过asn bypass
        @param context:
        @param index:
        @return:
        """
        tree = etree.HTML(context)
        left_list = tree.xpath(self.LEFT_LIST_RULE)
        asn_list = list()
        for i in range(len(left_list)):
            if len(left_list[i].xpath(self.ASN_RULE)) > 0:
                asn_data = left_list[i].xpath(self.ASN_RULE)[0].strip()
                if asn_data not in self.asn_list[index] and asn_data != None:
                    self.asn_list[index].add(asn_data)
                    asn_list.append(asn_data)
        print(asn_list)

        return asn_list

    def bypassOrg(self, context, index):
        """
        通过org bypass
        @param context:
        @param index:
        @return:
        """
        tree = etree.HTML(context)
        left_list = tree.xpath(self.LEFT_LIST_RULE)
        org_list = list()
        for i in range(len(left_list)):
            if len(left_list[i].xpath(self.ORG_RULE)) > 0:
                org_data = left_list[i].xpath(self.ORG_RULE)[0].strip()
                if org_data not in self.org_list[index] and org_data != None:
                    self.org_list[index].add(org_data)
                    org_list.append(org_data)
        print(org_list)
        return org_list

    def bypassCountry(self, context, index):
        """
        通过country bypass
        @param context:
        @param index:
        @return:
        """
        tree = etree.HTML(context)
        left_list = tree.xpath(self.LEFT_LIST_RULE)
        country_list = list()
        for i in range(len(left_list)):
            if len(left_list[i].xpath(self.CITY_RULE)) > 0:
                city_url = left_list[i].xpath(self.CITY_RULE)[0].strip()
                city = self.resetCityKeyword(city_url, "country")
                if city not in self.city_list[index] and city != None:
                    self.city_list[index].add(city)
                    country_list.append(city)
        print(country_list)
        return country_list

    def bypassPort(self, context, index):
        """
        通过port bypass
        @param context:
        @param index:
        @return:
        """
        tree = etree.HTML(context)
        data_list = tree.xpath(self.PORT_RULE)
        port_list = list()
        for port in data_list:
            port = port.strip()
            if port not in self.port_list[index] and port != None:
                # print(self.PORT_SET)
                self.port_list[index].add(port)
                port_list.append(port)
        print(port_list)
        return port_list

    def resetCityKeyword(self, keyURL, key):
        """
        重置城市关键字
        @param keyURL:
        @param key:
        @return:
        """
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

    def setIndexTimestamp(self, searchbs64, timestamp_index):
        """
        设置时间列表
        @param searchbs64:
        @param timestamp_index:
        @return:
        """
        try:
            request_url = 'https://fofa.info/result?qbase64=' + searchbs64 + "&full=false&page_size=10"
            # print(f'request_url:{request_url}')
            rep = requests.get(request_url, headers=fofa_useragent.getFofaPageNumHeaders(), timeout=self.timeout,
                               proxies=self.proxy)
            # print(rep.text)
            timelist = self.getTimeList(rep.text)
            # print(timelist)
            for temptime in timelist:
                self.timestamp_list[timestamp_index].add(temptime)
            return rep
        except Exception as e:
            print(e)
            pass
        return None

    def fofaSpiderOnePageData(self, search_key, searchbs64, timestamp_index):
        """
        获取fofa一页的数据
        :rtype: object
        """
        searchbs64 = searchbs64.replace("%3D", "=")
        # init_search_key = base64.b64decode(searchbs64).decode()
        init_search_key = search_key
        print("now search key: " + init_search_key)
        TEMP_RETRY_NUM = 0

        while TEMP_RETRY_NUM < self.MAX_MATCH_RETRY_NUM:
            try:
                rep = self.setIndexTimestamp(searchbs64, timestamp_index)
                self.saveDataToFile(rep)
                for url in self.level_data.format_data:
                    self.host_set.add(url)

                time.sleep(self.time_sleep)

                return rep.text

            except Exception as e:
                print("[-] error:{}".format(e))
                TEMP_RETRY_NUM += 1
                print('[-] 第{}次尝试获取页面URL'.format(TEMP_RETRY_NUM))
                pass

        print('[-] FOFA资源获取重试超过最大次数,程序退出')
        exit(0)

    def saveDataToFile(self, rep):
        """
        数据保存至文件
        @param rep:
        """
        self.level_data.startSpider(rep)
        # tree = etree.HTML(rep.text)
        # urllist = tree.xpath('//span[@class="hsxa-host"]/a/@href')
        print("[*] 已爬取条数 [{}]: ".format(len(self.host_set)) + str(self.level_data.format_data))

        self.output_data.output(self.level_data.format_data)
        # for i in self.level_data.formatData:
        #     with open(self.filename, 'a+', encoding="utf-8") as f:
        #         f.write(str(i) + "\n")

    def checkDataIsUpdate(self):
        """
        检测数据是否新增
            新增为 true
            未新增为 false
        @return:
        """
        return self.old_length != len(self.host_set)

    def fofaSpider(self, search_key, searchbs64, index):
        """
        爬取某关键字的fofa数据
        @param search_key:
        @param searchbs64:
        @param index:
        @return:
        """
        # while len(self.host_set) < self.endcount and self.old_length !=len(self.host_set):

        self.old_length = len(self.host_set)
        self.timestamp_list[index].clear()
        context = self.fofaSpiderOnePageData(search_key, searchbs64, index)

        if self.EXIT_FLAG:
            return

        if len(self.host_set) >= self.endcount:
            print("[*] 在{}节点,数据爬取结束".format(index))
            finalint = self.removeDuplicate()
            print('[*] 去重结束，最终数据 ' + str(finalint) + ' 条')
            self.EXIT_FLAG = True
            return
        if self.old_length == len(self.host_set):
            self.no_new_data_count += 1
            if self.no_new_data_count == 2:
                print("[-] {}节点数据无新增,该节点枯萎".format(index))
                return
        else:
            self.no_new_data_count = 0

        if self.fuzz:
            self.fofaFuzzSpider(search_key, context, index)

        search_key_modify = self.modifySearchTimeUrl(search_key, index)
        # print(search_key_modify)
        searchbs64_modify = quote_plus(base64.b64encode(search_key_modify.encode()))
        # search_key = search_key_modify
        # searchbs64 = searchbs64_modify
        self.fofaSpider(search_key_modify, searchbs64_modify, index)

    def isPortInKeyword(self):
        """
        检测输入关键字是否包含了port,目前看来有两种情况：
            1、"116.63.67.65:8009"
            2、host="116.63.67.65:8009"
        @return:
        """
        if " " not in self.search_key:
            if ":" in self.search_key:
                return False
        if "host" in self.search_key:
            result = re.findall('host="(.*?)"', self.search_key)
            if len(result) > 0 and ":" in result:
                return False
        return True

    def fuzzListAdd(self):
        """
        新增fuzz列表下标
        """
        self.timestamp_index += 1
        self.timestamp_list.append(set())
        self.city_list.append(set())
        self.asn_list.append(set())
        self.org_list.append(set())
        self.port_list.append(set())

    def fofaFuzzSpider(self, search_key, context, index):
        """
        递归调用 fofaSpider 方法不断 fuzz
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
                elif fuzzKey == "port" and self.isPortInKeyword():
                    dataList = self.bypassPort(context, index)
                else:
                    dataList = []
                # country_list = self.bypassCountry(context, index)
                for data in dataList:
                    new_key = search_key + ' && {}="{}"'.format(fuzzKey, data)
                    # print("new_key: "+new_key)
                    searchbs64_modify = quote_plus(base64.b64encode(new_key.encode("utf-8")))
                    self.fuzzListAdd()
                    self.setIndexTimestamp(searchbs64_modify, self.timestamp_index)
                    # self.fofaSpiderOnePageData(search_key,searchbs64_modify,self.timestamp_index)
                    self.fofaSpider(new_key, searchbs64_modify, self.timestamp_index)

                for data in dataList:
                    new_key = search_key + ' && {}!="{}"'.format(fuzzKey, data)
                    # print("new_key: "+new_key)
                    searchbs64_modify = quote_plus(base64.b64encode(new_key.encode("utf-8")))
                    self.fuzzListAdd()
                    self.setIndexTimestamp(searchbs64_modify, self.timestamp_index)
                    # self.fofaSpiderOnePageData(search_key,searchbs64_modify,self.timestamp_index)
                    self.fofaSpider(new_key, searchbs64_modify, self.timestamp_index)



    def modifySearchTimeUrl(self, search_key, index):
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

    def removeDuplicate(self):
        """
        去除重复值
        @return:
        """
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
        searchbs64 = self.getFofaKeywordsCount(self.search_key)
        self.fofaSpider(self.search_key, searchbs64, 0)
        print('[*] 抓取结束，共抓取数据 ' + str(len(self.host_set)) + ' 条\n')

    def mainCall(self,keyword="test",timeSleep=3,timeout=3,endcount=100,level="1",fuzz=False,
                  output="txt",proxy=None):
        """
        外部调用fofa-hack 使用此方法
        返回self.host_set
        :param keyword:
        :param timeSleep:
        :param timeout:
        :param endcount:
        :param level:
        :param fuzz:
        :param output:
        :param proxy:
        :return:
        """
        self.timeSleep = int(timeSleep)
        self.timeout = int(timeout)
        self.searchKey = self.clipKeyWord(keyword)
        self.endcount = int(endcount)
        self.level = level
        self.levelData = LevelData(self.level)
        self.fuzz = fuzz
        self.output = output
        self.filename = "{}_{}.{}".format(unit.md5(self.searchKey), int(time.time()), self.output)
        self.outputData = OutputData(self.filename, self.level, pattern=self.output)
        self.proxy = self.setProxy(proxy)
        self.outInitMsg()
        searchbs64 = base64.b64encode(f'{self.searchKey}'.encode()).decode()
        self.fofaSpider(self.searchKey, searchbs64, 0)
        print('[*] 抓取结束，共抓取数据 ' + str(len(self.host_set)) + ' 条\n')
        print(self.host_set)

        return self.host_set


if __name__ == '__main__':
    fofa = Fofa()
    fofa.main()