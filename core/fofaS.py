#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/5/30 20:59
# @Author  : Cl0udG0d
# @File    : fofaS.py
# @Github: https://github.com/Cl0udG0d
from datetime import datetime
from datetime import timedelta
import base64
import time
from urllib.parse import quote_plus
from tookit import unit, fofaUseragent
from tookit.fofaUseragent import getFofaPageNumHeaders
from tookit.levelData import LevelData
from tookit.outputData import OutputData
import re, requests
from lxml import etree

from tookit.unit import clipKeyWord, setProxy, get_username
from selenium import webdriver
from selenium.webdriver.common.by import By
import ddddocr
from selenium.webdriver.support.wait import WebDriverWait
from tookit.autoEmail import Emailnator


class FofaS:
    '''
    FUZZ规则
    '''
    LEFT_LIST_RULE = '//div[@class="hsxa-meta-data-list-main-left hsxa-fl"]'
    CITY_RULE = 'p[3]/a/@href'
    ASN_RULE = 'p[4]/a/text()'
    ORG_RULE = 'p[5]/a/text()'
    PORT_RULE = '//a[@class="hsxa-port"]/text()'

    def __init__(self, search_key, inputfile, filename, time_sleep, endcount, level, level_data, output, output_data,
                 fuzz, timeout, is_proxy, proxy):
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

        self.driver = self.initDriver()

        self.bypass = None
        self.host_set = set()
        self.timestamp_list = list()
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
        self.EXIT_FLAG = False

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
[*] {"从" + self.inputfile if self.inputfile else "不从"}文件中读取
''')

    def getFofaKeywordsCount(self):
        """
        获取关键字的搜索数量值
        :param search_key:
        :return:
        """
        WebDriverWait(self.driver, timeout=5).until(lambda d: d.find_element(By.CLASS_NAME, 'inner'))
        self.driver.get('https://octra.fofa.vip/technologyStack/fofa')

        self.driver.find_element(by=By.CLASS_NAME, value='el-input__inner').send_keys(self.search_key)
        self.driver.find_element(by=By.CLASS_NAME, value='el-button').click()

        WebDriverWait(self.driver, timeout=5).until(
            lambda d: d.find_element(By.XPATH, '//span[@class="hsxa-highlight-color"]'))

        countnum = self.driver.find_elements(by=By.XPATH, value='//span[@class="hsxa-highlight-color"]')[0].text
        print("[*] 存在数量:" + countnum)

        # for i in datalist:
        #     print(i.get_attribute("href"))
        #
        # self.driver.find_element(by=By.CLASS_NAME, value='btn-next').click()

        # searchbs64 = base64.b64encode(f'{search_key}'.encode()).decode()
        # print("[*] 爬取页面为:https://fofa.info/result?qbase64=" + searchbs64)
        # html = requests.get(url="https://fofa.info/result?qbase64=" + searchbs64,
        #                     headers=fofaUseragent.getFofaPageNumHeaders(), timeout=self.timeout,proxies=self.proxy)\
        #                     .text
        # tree = etree.HTML(html)
        # try:
        #     countnum = tree.xpath('//span[@class="hsxa-highlight-color"]/text()')[0]
        #     # standaloneIpNum = tree.xpath('//span[@class="hsxa-highlight-color"]/text()')[1]
        # except Exception as e:
        #     print("[-] error:{}".format(e))
        #     countnum = '0'
        #     pass
        # # print("[*] 独立IP数量:" + standaloneIpNum)
        # return searchbs64

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

    def fofaSpiderOnePageData(self):
        """
        获取fofa一页的数据
        :rtype: object
        """
        WebDriverWait(self.driver, timeout=20).until(lambda d: d.find_element(By.XPATH, '//span[@class="hsxa-host"]/a'))
        time.sleep(self.time_sleep)
        datalist = self.driver.find_elements(by=By.XPATH, value='//span[@class="hsxa-host"]/a')
        data_list = list()
        for i in datalist:
            data_list.append(i.get_attribute("href"))

        print(data_list)
        self.saveDataToFile(data_list)
        for url in data_list:
            self.host_set.add(url)

        timelist = self.getTimeList(self.driver.page_source)
        self.timestamp_list.extend(timelist)

        # time.sleep(self.time_sleep)

    def saveDataToFile(self, data_list):
        """
        数据保存至文件
        @param rep:
        """
        # self.level_data.startSpider(rep)
        # tree = etree.HTML(rep.text)
        # urllist = tree.xpath('//span[@class="hsxa-host"]/a/@href')
        print("[*] 已爬取条数 [{}]: ".format(len(self.host_set)) + str(data_list))

        self.output_data.output(data_list)
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

    def fofaSpider(self):
        """
        爬取某关键字的fofa数据
        """
        WebDriverWait(self.driver, timeout=5).until(lambda d: d.find_element(By.CLASS_NAME, 'el-input__inner'))
        self.driver.get('https://fofa.info/')

        self.driver.find_element(by=By.CLASS_NAME, value='el-input__inner').send_keys(self.search_key)
        self.driver.find_element(by=By.CLASS_NAME, value='icon-search').click()
        count_flag = 0

        while len(self.host_set) < self.endcount:
            if count_flag == 5:
                count_flag = 0
                self.search_key = self.modifySearchTimeUrl(self.search_key)
                input_button = self.driver.find_element(by=By.CLASS_NAME, value='el-input__inner')
                input_button.clear()
                input_button.send_keys(self.search_key)
                self.driver.find_element(by=By.CLASS_NAME, value='icon-search').click()
                self.timestamp_list.clear()

            self.old_length = len(self.host_set)
            self.fofaSpiderOnePageData()
            next_page_button = self.driver.find_elements(by=By.XPATH,
                                                         value='//div[@class="hsxa-pagination el-pagination"]/button[@class="btn-next"]')[
                1]
            next_page_button.click()
            count_flag += 1

        finalint = self.removeDuplicate()
        print('[*] 去重结束，最终数据 ' + str(finalint) + ' 条')

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

    def modifySearchTimeUrl(self, search_key):
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
        timestamp_list = list(self.timestamp_list)
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

    def registerFofa(self):
        self.driver.get('https://i.nosec.org/register')
        WebDriverWait(self.driver, timeout=5).until(lambda d: d.find_element(By.LINK_TEXT, 'NOSEC'))
        ocr = ddddocr.DdddOcr(show_ad=False)
        authimgbox = self.driver.find_element('xpath', '//*[@id="captcha_image"]')
        imgb = authimgbox.screenshot_as_png
        captcha = ocr.classification(imgb)
        print(captcha)
        if len(captcha) != 5:
            print("验证码输入错误")
            self.registerFofa()

        mail_client = Emailnator()
        # mail_address = mail_client.get_mail()
        self.nosecuser_email = mail_client.get_mail()

        self.nosecuser_username = get_username()
        self.nosecuser_password = "Test12345678"

        print("email {} , username {} , password {}".format(self.nosecuser_email, self.nosecuser_username,
                                                            self.nosecuser_password))
        self.driver.find_element(by=By.ID, value='nosecuser_email').send_keys(self.nosecuser_email)
        self.driver.find_element(by=By.ID, value='nosecuser_username').send_keys(self.nosecuser_username)
        self.driver.find_element(by=By.ID, value='nosecuser_password').send_keys(self.nosecuser_password)
        self.driver.find_element(by=By.ID, value='nosecuser_password_confirmation').send_keys(self.nosecuser_password)
        self.driver.find_element(by=By.NAME, value='_rucaptcha').send_keys(captcha)
        time.sleep(1)
        self.driver.find_element(by=By.NAME, value='commit').click()
        time.sleep(5)
        # mail_content = mail_client.get_message()
        # print(mail_content)
        confirm_link = mail_client.get_confirm_link()

        # 链接确认
        requests.get(confirm_link, timeout=5, headers=getFofaPageNumHeaders())
        time.sleep(1)

    def loginGAFofa(self):
        self.driver.get('https://i.nosec.org/login?locale=zh-CN&service=https://fofa.info/f_login')
        WebDriverWait(self.driver, timeout=10).until(lambda d: d.find_element(By.LINK_TEXT, 'FOFA'))
        ocr = ddddocr.DdddOcr(show_ad=False)
        authimgbox = self.driver.find_element('xpath', '//*[@id="captcha_image"]')
        imgb = authimgbox.screenshot_as_png
        captcha = ocr.classification(imgb)
        time.sleep(5)
        if len(captcha) != 5:
            print("验证码输入错误")
            self.loginGAFofa()
        time.sleep(3)

        self.driver.find_element(by=By.ID, value='username').send_keys(self.nosecuser_email)
        self.driver.find_element(by=By.ID, value='password').send_keys(self.nosecuser_password)
        self.driver.find_element(by=By.NAME, value='_rucaptcha').send_keys(captcha)
        self.driver.find_element(by=By.ID, value='fofa_service').click()
        time.sleep(1)
        self.driver.find_element(by=By.NAME, value='button').click()
        if '登录验证码错误' in self.driver.page_source:
            print("验证码错误，重新运行脚本")
            self.loginGAFofa()
        elif '用户名或密码错误' in self.driver.page_source:
            print('用户名或密码错误,请检查账户名和密码后重试')
            return
        else:
            print("登录成功")

    def initDriver(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option('detach', True)
        options.add_argument('--start-maximized')
        driver = webdriver.Chrome(options=options)
        return driver

    def start(self):
        self.outInitMsg()
        print('[*] 开始运行')
        self.registerFofa()
        self.loginGAFofa()
        # self.getFofaKeywordsCount()
        self.fofaSpider()
        print('[*] 抓取结束，共抓取数据 ' + str(len(self.host_set)) + ' 条\n')

        # WebDriverWait(self.driver, timeout=5).until(lambda d: d.find_element(By.CLASS_NAME, 'inner'))
        # self.driver.get('https://octra.fofa.vip/technologyStack/fofa')
        #
        # self.driver.find_element(by=By.CLASS_NAME, value='el-input__inner').send_keys(self.search_key)
        # self.driver.find_element(by=By.CLASS_NAME, value='el-button').click()
        #
        # WebDriverWait(self.driver, timeout=5).until(lambda d: d.find_element(By.XPATH, '//span[@class="hsxa-host"]/a'))
        #
        # datalist = self.driver.find_elements(by=By.XPATH, value='//span[@class="hsxa-host"]/a')
        # for i in datalist:
        #     print(i.get_attribute("href"))
        #
        # self.driver.find_element(by=By.CLASS_NAME, value='btn-next').click()

        # if self.inputfile:
        #     with open(self.inputfile, 'r') as f:
        #         for line in f.readlines():
        #             self.cleanInitParameters()
        #             self.search_key = clipKeyWord(line.strip())
        #             self.filename = "{}_{}.{}".format(unit.md5(self.search_key), int(time.time()), self.output)
        #             self.output_data = OutputData(self.filename, self.level, pattern=self.output)
        #             searchbs64 = self.getFofaKeywordsCount(self.search_key)
        #             self.fofaSpider(self.search_key, searchbs64, 0)
        #             print(f'[*] 抓取结束，{self.search_key}关键字共抓取数据 ' + str(len(self.host_set)) + ' 条\n')
        # else:
        #     searchbs64 = self.getFofaKeywordsCount(self.search_key)
        #     self.fofaSpider(self.search_key, searchbs64, 0)
        #     print('[*] 抓取结束，共抓取数据 ' + str(len(self.host_set)) + ' 条\n')


if __name__ == '__main__':
    fofa = FofaS("index", None, "aaa.txt", 3, 100, 1, LevelData(), "txt", OutputData("aaa"), False,
                 5, False, None)
    fofa.start()
