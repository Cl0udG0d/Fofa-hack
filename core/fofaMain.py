#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/9/24 22:13
# @Author  : Cl0udG0d
# @File    : fofaMain.py
# @Github: https://github.com/Cl0udG0d
import json
import os
import random
import sys
import urllib
from datetime import datetime
from datetime import timedelta
import base64
import time
from urllib.parse import quote_plus
from tookit import unit, fofaUseragent, config
from tookit.client_main import get_result_from_api
from tookit.levelData import LevelData
from tookit.outputData import OutputData
import re, requests
from lxml import etree

from tookit.sign import getUrl
from tookit.unit import clipKeyWord, colorize
import gettext
import locale

if getattr(sys, 'frozen', None):
    dir = sys._MEIPASS
else:
    dir = config.ROOT_PATH
# 获取当前的语言设置
lang, _ = locale.getdefaultlocale()
if lang.startswith('zh'):
    # 如果是中文环境，不需要翻译，直接用原始字符串
    _ = lambda x: x
else:
    # 如果是其他语言环境，则加载对应的翻译文件
    language = gettext.translation('fofa_hack', localedir=os.path.join(dir, "locale"), languages=['en'])
    language.install()
    _ = language.gettext


class FofaMain:
    '''
    FUZZ规则
    '''
    LEFT_LIST_RULE = '//div[@class="hsxa-meta-data-list-main-left hsxa-fl"]'
    CITY_RULE = 'p[3]/a/@href'
    ASN_RULE = 'p[4]/a/text()'
    ORG_RULE = 'p[5]/a/text()'
    PORT_RULE = '//a[@class="hsxa-port"]/text()'

    def __init__(self, search_key, inputfile, filename, time_sleep, endcount, level, level_data, output, output_data,
                 fuzz, timeout, is_proxy, proxy=None):
        """
        初始化方法
        """
        self.search_key = search_key
        self.inputfile = inputfile
        self.filename = filename
        self.time_sleep = time_sleep
        self.endcount = endcount
        self.level = level
        self.level_data = level_data
        self.output = output
        self.output_data = output_data
        self.fuzz = fuzz
        self.timeout = timeout
        self.is_proxy = is_proxy
        self.proxy = proxy

        self.bypass = None
        self.host_set = set()
        self.timestamp_list = [set()]
        self.city_list = [set()]
        self.asn_list = [set()]
        self.org_list = [set()]
        self.port_list = [set()]
        self.old_length = -1

        self.country_list = []
        self.timestamp_index = 0
        self.no_new_data_count = 0
        # 登录最大重试次数
        self.MAX_LOGIN_RETRY_NUM = 3
        # 页面URL获取最大重试次数
        self.MAX_MATCH_RETRY_NUM = 3

        # 当前页码
        self.current_page_num = 1
        self.EXIT_FLAG = False

    def outInitMsg(self):
        """
        输出初始化信息
        """
        print(colorize(_('''[*] LEVEL = {} , 初始化成功
[*] 爬取延时: {}s
[*] 爬取关键字: {}
[*] 爬取结束数量: {}
[*] 输出格式为: {}
[*] 存储文件名: {}
[*] 是否开启关键字fuzz: {}
[*] 是否开启代理: {}
[*] 读取文件: {}
''').format(self.level, self.time_sleep, self.search_key, self.endcount, self.output, self.filename,
            self.fuzz, self.is_proxy, self.inputfile), "green"))

    def format_single_proxy(self, proxy):
        """
        格式化单个代理
        """
        proxies = {}
        if proxy:
            proxies = {
                'http': config.PROXY_TYPE + '://' + proxy,
                'https': config.PROXY_TYPE + '://' + proxy
            }
            return proxies
        else:
            return proxies

    def get_proxy(self):
        # 防止有通过API调用FOFA的情况
        if self.proxy:
            return self.proxy

        if config.IS_PROXY:
            if config.PROXY_SINGLE:
                return self.format_single_proxy(config.PROXY_ARGS)
            elif config.PROXY_FROM_TXT:
                file_path = os.path.join(config.ROOT_PATH, config.PROXY_ARGS)

                # 读取文件中的所有行
                with open(file_path, 'r') as file:
                    lines = file.readlines()

                proxy = random.choice(lines).strip()
                return self.format_single_proxy(proxy)
            else:
                rep = requests.get(config.PROXY_ARGS, headers=fofaUseragent.getNormalHeaders(), timeout=10)
                if rep:
                    proxy = rep.text.strip()
                    return self.format_single_proxy(proxy)
                else:
                    return {}
        else:
            return {}

    def getFofaKeywordsCount(self, search_key):
        """
        获取关键字的搜索数量值
        :param search_key:
        :return:
        """
        searchbs64 = base64.b64encode(f'{search_key}'.encode()).decode()
        print(colorize(_("[*] 爬取页面为:https://fofa.info/result?qbase64={}").format(searchbs64), "green"))
        if config.AUTHORIZATION:
            return searchbs64, ""
        try:

            html = requests.get(url="https://fofa.info/result?qbase64=" + searchbs64,
                                headers=fofaUseragent.getFofaPageNumHeaders(), timeout=self.timeout,
                                proxies=self.get_proxy()) \
                .text
            tree = etree.HTML(html)
            countnum = tree.xpath('//span[@class="hsxa-highlight-color"]/text()')[0]
            # standaloneIpNum = tree.xpath('//span[@class="hsxa-highlight-color"]/text()')[1]
        except Exception as e:
            print("\033[1;31m[-] error:{}\033[0m".format(e))
            countnum = '0'
            print(
                "\033[1;31m[-] perhaps there is a problem with your network or your area has been officially banned by Fofa, so the program exits\033[0m")
            self._destroy()
        print(colorize(_("[*] 存在数量:{}").format(countnum), "green"))
        # print("[*] 独立IP数量:" + standaloneIpNum)
        return searchbs64, countnum

    def getTimeList(self, text):
        """
        获取时间列表
        :param text:
        :return:
        """
        timelist = list()
        data = json.loads(text)
        assets = data["data"]["assets"]
        for asset in assets:
            mtime = asset["mtime"].split()[0]
            timelist.append(mtime)
        # print(timelist)
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

    def check_authorization_is_available(self):

        # au = config.AUTHORIZATION_LIST.pop()
        # print(au)
        # print(config.AUTHORIZATION_LIST)
        while len(config.AUTHORIZATION_LIST)>0:
            config.AUTHORIZATION = config.AUTHORIZATION_LIST.pop()

            try:
                request_profile_url = "https://api.fofa.info/v1/m/profile"
                rep = requests.get(request_profile_url, headers=fofaUseragent.getFofaPageNumHeaders(), timeout=10)
                limit_num = json.loads(rep.text)["data"]["info"]["data_limit"]["web_data"]

                request_month_url = "https://api.fofa.info/v1/m/data_usage/month"
                rep = requests.get(request_month_url, headers=fofaUseragent.getFofaPageNumHeaders(), timeout=10)
                available_num = json.loads(rep.text)["data"]["web_data"]

                if available_num + 50 < limit_num:
                    config.AUTHORIZATION_LIST.append(config.AUTHORIZATION)
                    return True

            except Exception as e:
                print(
                    "\033[1;31m[-] error:AUTHORIZATION测试错误 {}\033[0m".format(e))
                pass
        return False

    def setIndexTimestamp(self, searchbs64, timestamp_index):
        """
        设置时间列表
        @param searchbs64:
        @param timestamp_index:
        @return:
        """
        try:
            if config.AUTHORIZATION_FILE:
                if not self.check_authorization_is_available():
                    print("\033[1;31m[-] error:{}\033[0m".format(
                        "authorization获取数据均达本月上限或authorization存在错误"))
                    exit(0)

            request_url = getUrl(searchbs64)
            if config.DEBUG:
                print("[+] 当前请求网址: "+request_url)

            rep = requests.get(request_url, headers=fofaUseragent.getFofaPageNumHeaders(), timeout=self.timeout,
                               proxies=self.get_proxy())
            # request should be success
            rep.raise_for_status()
            if config.DEBUG:
                print("[+] 当前响应: " + rep.text)
            # request should not be limited
            # '{"code":820006,"message":"[820006] 资源访问每天限制","data":""}'
            if len(rep.text) <= 55 and '820006' in rep.text:
                raise RuntimeError("\033[1;31m[-] error:{}\033[0m".format(
                        "API call limit reached for today,call at next day or use proxy"))
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
        # searchbs64 = searchbs64.replace("%3D", "=")
        # init_search_key = base64.b64decode(searchbs64).decode()
        init_search_key = search_key
        # if not config.AUTHORIZATION:
        print("\033[1;34mnow search key: {}\033[0m".format(init_search_key))
        TEMP_RETRY_NUM = 0

        while TEMP_RETRY_NUM < self.MAX_MATCH_RETRY_NUM:
            try:
                rep = self.setIndexTimestamp(searchbs64, timestamp_index)
                self.saveDataToFile(rep)
                for data in self.level_data.format_data:
                    if self.level == "1":
                        self.host_set.add(data)
                    elif self.level == "2":
                        self.host_set.add(data["url"])
                    else:
                        self.host_set.add(data["id"])

                time.sleep(self.time_sleep)

                return rep.text if rep else None

            except Exception as e:
                print("\033[1;31m[-] error:{}\033[0m".format(e))
                TEMP_RETRY_NUM += 1
                print(colorize(_('[-] 第{}次尝试获取页面URL').format(TEMP_RETRY_NUM), "red"))
                # pass

        print(colorize(_('[-] FOFA资源获取重试超过最大次数,程序退出'), "red"))
        self._destroy()

    def saveDataToFile(self, rep):
        """
        数据保存至文件
        @param rep:
        """
        self.level_data.startSpider(rep)
        # tree = etree.HTML(rep.text)
        # urllist = tree.xpath('//span[@class="hsxa-host"]/a/@href')
        print(
            colorize(_("[*] 已爬取条数 {} : {}").format(len(self.host_set), str(self.level_data.format_data)), "green"))

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
            print(colorize(_("[*] 在{}节点,数据爬取结束").format(index), "green"))
            if self.output == 'txt':
                finalint = self.removeDuplicate()
                print(colorize(_('[*] 去重结束，最终数据 {} 条').format(str(finalint)), "green"))
            else:
                print(colorize(_('[*] 输出类型为其他,不进行去重操作 '), "green"))
            self.EXIT_FLAG = True
            return
        if self.old_length == len(self.host_set):
            self.no_new_data_count += 1
            if self.no_new_data_count == 2:
                print(colorize(_("[-] {}节点数据无新增,该节点枯萎").format(index), "red"))
                return
        else:
            self.no_new_data_count = 0

        if self.fuzz and not self.EXIT_FLAG:
            self.fofaFuzzSpider(search_key, context, index)

        search_key_modify = self.modifySearchTimeUrl(search_key, index)
        # print(search_key_modify)
        searchbs64_modify = urllib.parse.quote(base64.b64encode(search_key_modify.encode("utf-8")))
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
                    searchbs64_modify = urllib.parse.quote(base64.b64encode(new_key.encode("utf-8")))
                    self.fuzzListAdd()
                    self.setIndexTimestamp(searchbs64_modify, self.timestamp_index)
                    # self.fofaSpiderOnePageData(search_key,searchbs64_modify,self.timestamp_index)
                    self.fofaSpider(new_key, searchbs64_modify, self.timestamp_index)

                for data in dataList:
                    new_key = search_key + ' && {}!="{}"'.format(fuzzKey, data)
                    # print("new_key: "+new_key)
                    searchbs64_modify = urllib.parse.quote(base64.b64encode(new_key.encode("utf-8")))
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
        if len(timestamp_list) == 0:
            print(colorize(_("似乎时间戳到了尽头."), "red"))
            self._destroy()
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
        try:
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
        except FileNotFoundError:
            print("\033[1;31m[-] 未保存文件,去重失败\033[0m")
        except Exception as e:
            print("\033[1;31m[-] error:{}\033[0m".format(e))
            return 0

    def cleanInitParameters(self):
        """
        清理初始化参数,将它们都恢复初始状态
        """
        self.host_set = set()
        self.timestamp_list = [set()]
        self.city_list = [set()]
        self.asn_list = [set()]
        self.org_list = [set()]
        self.port_list = [set()]
        self.old_length = -1
        self.country_list = []
        self.timestamp_index = 0
        self.no_new_data_count = 0
        self.EXIT_FLAG = False

    def start(self):
        self.outInitMsg()
        print(colorize(_('[*] 开始运行'), "green"))
        if self.inputfile:
            with open(self.inputfile, 'r') as f:
                for line in f.readlines():
                    self.cleanInitParameters()
                    self.search_key = clipKeyWord(line.strip())
                    self.filename = "{}_{}.{}".format(unit.md5(self.search_key), int(time.time()), self.output)
                    self.output_data = OutputData(self.filename, self.level, pattern=self.output)
                    searchbs64, countnum = self.getFofaKeywordsCount(self.search_key)
                    if str(countnum) == "0" and len(str(countnum)) == 1:
                        print(colorize(_('无搜索结果，执行下一条'), "red"))
                        continue
                    else:
                        if config.FOFA_KEY:
                            get_result_from_api(self.search_key)
                        else:
                            self.fofaSpider(self.search_key, searchbs64, 0)
                            print(colorize(_('[+] 抓取结束,{}关键字共抓取数据 {} 条\n').format(self.search_key,
                                                                                               str(len(self.host_set))),
                                           "green"))

        else:
            searchbs64, countnum = self.getFofaKeywordsCount(self.search_key)
            if str(countnum) == "0" and len(str(countnum)) == 1:
                print(colorize(_('无搜索结果'), "red"))
            else:
                if config.FOFA_KEY:
                    get_result_from_api(self.search_key)
                else:
                    self.fofaSpider(self.search_key, searchbs64, 0)
                    print(colorize(_('[*] 抓取结束，共抓取数据 {} 条').format(str(len(self.host_set))), "green"))

    def _destroy(self):
        self.removeDuplicate()
        sys.exit(0)


if __name__ == '__main__':
    fofa = FofaMain("", "", "", 3, "", "", "", "", "", "", 10, "", "")
    fofa.setIndexTimestamp("InRoaW5rcGhwIg==", 0)
