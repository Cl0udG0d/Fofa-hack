#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/9/14 22:20
# @Author  : Cl0udG0d
# @File    : fofa.py
# @Github: https://github.com/Cl0udG0d
from datetime import datetime
from datetime import timedelta
import random
import base64
import time
from urllib.parse import quote_plus
import config
from urllib.parse import quote

host_list = []
timestamp_list = []

import re, requests

from lxml import etree

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.9 Safari/537.36',
    'Host': 'i.nosec.org',
    'Referer': 'https://i.nosec.org/login',
    'sec-ch-ua': '"Chromium";v="106", "Microsoft Edge";v="106", "Not;A=Brand";v="99"',
    'sec-ch-ua-platform': '"Windows"',
}


class Fofa:
    def __init__(self):
        self.session = requests.session()
        print('''
         ____  ____  ____  ____      
        | ===|/ () \| ===|/ () \     
        |__|  \____/|__| /__/\__\    
             _   _   ____   ____  __  __ 
            | |_| | / () \ / (__`|  |/  /
            |_| |_|/__/\__\\\\____)|__|\__\\
        ''')

    def fofa_captcha(self, src):
        import ddddocr
        ocr = ddddocr.DdddOcr(show_ad=False)
        fofa_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.9 Safari/537.36',
            'Host': 'i.nosec.org',
            'Referer': 'https://i.nosec.org/login',
            'sec-ch-ua': '"Chromium";v="106", "Microsoft Edge";v="106", "Not;A=Brand";v="99"',
            'sec-ch-ua-platform': '"Windows"',
        }
        captcha_api = f'https://i.nosec.org{src}'
        resp = self.session.get(url=captcha_api, headers=fofa_headers)
        return ocr.classification(resp.content)

    def fofa_login(self, fofa_username, fofa_password):
        print('尝试登录')
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.9 Safari/537.36',
            'Referer': 'https://i.nosec.org/login?service=https://fofa.info/f_login',
            'Host': 'i.nosec.org',
            'Origin': 'https://i.nosec.org',
            'sec-ch-ua': '"Chromium";v="106", "Microsoft Edge";v="106", "Not;A=Brand";v="99"',
            'sec-ch-ua-platform': '"Windows"',
        }

        authen = self.session.get(url='https://i.nosec.org/login?service=https://fofa.info/f_login', headers=headers)
        src = re.findall('class="rucaptcha-image" src="(.*?)"', authen.text)[0]

        captcha = self.fofa_captcha(src)
        authenticity_token = re.findall('"csrf-token" content="(.*?)" /', authen.text)[0]
        lt = re.findall('id="lt" value="(.*?)" /', authen.text)[0]
        data = {
            'utf8': '%E2%9C%93',
            'authenticity_token': authenticity_token,
            'lt': lt,
            'service': 'https://fofa.info/f_login',
            'username': fofa_username,
            'password': fofa_password,
            '_rucaptcha': captcha,
            'rememberMe': '1',
            'button': '',
            'fofa_service': '1',
        }
        user_login_api = 'https://i.nosec.org/login'
        res_login = self.session.post(url=user_login_api, data=data)
        if '登录验证码错误' in res_login.text:
            print("验证码错误，重新运行脚本")
            return 0
        elif '用户名或密码错误' in res_login.text:
            print('用户名或密码错误,请检查账户名和密码后重试')
            return 0
        else:
            print("登录成功")
            tempstr = ''
            for key, value in self.session.cookies.get_dict().items():
                tempstr += key + "=" + value + "; "
            print(tempstr)
            with open('fofa_cookie.txt', 'w') as f:
                f.write(tempstr)
            return self.session.cookies, 1

    def check_login(self, cookies):
        self.check_headers = {
            'Host': 'fofa.info',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.9 Safari/537.36',
            'sec-ch-ua': '"Chromium";v="106", "Microsoft Edge";v="106", "Not;A=Brand";v="99"',
            'sec-ch-ua-platform': '"Windows"',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'DNT': '1',
            'Referer': 'https://fofa.info/',
            'Connection': 'keep-alive',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Cookie': cookies,
        }
        resp = requests.get(url='https://fofa.info/result?qbase64=MQ==&page=2&page_size=10', headers=self.check_headers)
        tree = etree.HTML(resp.text)
        urllist = tree.xpath('//span[@class="hsxa-host"]/a/@href')
        return len(urllist), cookies

    def cookie_info(self):
        """
        读取cookie
        :rtype: object
        """
        with open('fofa_cookie.txt', 'r') as f:
            cookies = f.read()
            return cookies if cookies!='' else ''

    def headers(self,cookie):
        user_agent_use = config.user_agent[random.randint(0, len(config.user_agent) - 1)]
        headers_use = {
            'User-Agent': user_agent_use,
            'Accept': 'application/json, text/plain, */*',
            "cookie": cookie.encode("utf-8").decode("latin1")
        }
        return headers_use


    def init(self):
        config.TimeSleep = int(input('[*] 请输入爬取每一页等待的秒数，防止IP被ban\n'))
        config.SearchKEY = input('[*] 请输入fofa搜索关键字 \n')
        return

    def get_page_num(self, search_key,cookie):
        # 获取页码
        headers_use = self.headers(cookie)
        searchbs64 = base64.b64encode(f'{search_key}'.encode()).decode()
        print("[*] 爬取页面为:https://fofa.info/result?qbase64=" + searchbs64)
        html = requests.get(url="https://fofa.info/result?qbase64=" + searchbs64, headers=headers_use).text
        tree = etree.HTML(html)
        try:
            pagenum = tree.xpath('//li[@class="number"]/text()')[-1]
        except Exception as e:
            print(e)
            pagenum = '0'
            pass
        print("[*] 存在页码:" + pagenum)
        return searchbs64, headers_use

    def getTimeList(self, text):
        # 获取时间列表
        timelist = list()
        pattern = "<span>[0-9]*-[0-9]*-[0-9]*</span>"
        result = re.findall(pattern, text)
        for temp in result:
            timelist.append(temp.replace("<span>", "").replace("</span>", "").strip())
        return timelist

    def fofa_spider_page(self, page, search_key, searchbs64, headers_use, turn_num):
        # 获取
        global host_list
        global timestamp_list
        searchurl = quote_plus(search_key)  # searchurl是search_key url encode
        searchurl = searchurl.replace('%28', '(').replace('%29', ')')
        print("[*] 正在爬取第" + str(5 * int(turn_num) + int(page)) + "页")
        request_url = 'https://fofa.info/result?qbase64=' + searchbs64 + '&full=false&page=' + str(
            page) + "&page_size=10"
        # print(f'request_url:{request_url}')
        rep = requests.get(request_url, headers=headers_use)
        tree = etree.HTML(rep.text)
        urllist = tree.xpath('//span[@class="hsxa-host"]/a/@href')
        timelist = self.getTimeList(rep.text)
        print(urllist)
        for i in urllist:
            with open('spider_result.txt', 'a+') as f:
                f.write(i + "\n")
        host_list.extend(urllist)
        timestamp_list.extend(timelist)

        time.sleep(config.TimeSleep)
        return

    def fofa_spider(self, search_key, searchbs64, headers_use):
        global host_list

        start_page = input("[*] 请输入开始页码: ")
        want_page = input("[*] 请输入终止页码: ")
        if int(want_page) <= 5 and int(want_page) > 0:
            stop_page = want_page
            for page in range(int(start_page), int(stop_page) + 1):
                self.fofa_spider_page(page, search_key, searchbs64, headers_use, turn_num=0)
        elif int(want_page) > 5:
            if int(want_page) % 5 == 0:
                start_page = start_page
                stop_page = 5
                for turn_num in range(int(int(want_page) / 5)):
                    global timestamp_list
                    # print('[*] 第 ' + str(turn_num + 1) + ' turn抓取')
                    timestamp_list.clear()
                    for page in range(int(start_page), int(stop_page) + 1):
                        self.fofa_spider_page(page, search_key, searchbs64, headers_use, turn_num)

                    search_key_modify, searchbs64_modify = self.modify_search_url(search_key)
                    search_key = search_key_modify
                    searchbs64 = searchbs64_modify
            else:
                turn_sum = int(want_page) // 5
                page_last = int(want_page) % 5
                for turn_num in range(int(want_page) // 5):
                    start_page = start_page
                    stop_page = 5
                    # print('[*] 第 ' + str(turn_num + 1) + ' turn抓取')
                    timestamp_list.clear()
                    for page in range(int(start_page), int(stop_page) + 1):
                        self.fofa_spider_page(page, search_key, searchbs64, headers_use, turn_num)

                    search_key_modify, searchbs64_modify = self.modify_search_url(search_key)
                    search_key = search_key_modify
                    searchbs64 = searchbs64_modify
                for page in range(1, page_last + 1):
                    # print('[*] 第 ' + str(turn_num + 2) + ' turn抓取')
                    self.fofa_spider_page(page, search_key, searchbs64, headers_use, turn_num=turn_sum)
        else:
            print('[-] 输入错误')
            exit(0)
        return

    def modify_search_url(self, search_key):
        global timestamp_list
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

        searchbs64_modify = quote_plus(base64.b64encode(search_key_modify.encode()))
        # print('[*] 搜索词： ' + search_key_modify)

        return search_key_modify, searchbs64_modify

    def run(self, cookie):
        self.init()
        searchbs64, headers_use = self.get_page_num(config.SearchKEY,cookie)
        self.fofa_spider(config.SearchKEY, searchbs64, headers_use)
        print('[+] 抓取结束，共抓取数据 ' + str(len(host_list)) + ' 条\n')

    def main(self):
        print('检测是否登录')
        urllist, cookie = self.check_login(self.cookie_info())
        if urllist == 0:
            print("未登录")
            if self.fofa_login(config.fofa_username, config.fofa_password)[1] == 1:
                print('开始搜索')
                self.run(self.cookie_info())
                print('退出')
            else:
                exit(0)
        else:
            print('已经登录')
            self.run(cookie)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()


if __name__ == '__main__':
    fofa = Fofa()
    fofa.main()
