#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2022/9/14 22:20
# @Author  : Cl0udG0d
# @File    : fofa.py
# @Github: https://github.com/Cl0udG0d
import datetime
from datetime import datetime
from datetime import timedelta
import random
import base64
import re
import time

from lxml import etree
import requests
from urllib.parse import quote_plus
import config

host_list = []
timestamp_list = []

def logo():
    print('''
     ____  ____  ____  ____      
    | ===|/ () \| ===|/ () \     
    |__|  \____/|__| /__/\__\    
         _   _   ____   ____  __  __ 
        | |_| | / () \ / (__`|  |/  /
        |_| |_|/__/\__\\\\____)|__|\__\\
    ''')

def checkSession():
    if config.cookie=="":
        print("[-] 请配置config文件cookie字段")
        exit(0)
    print("[*] 检测cookie成功")
    return

def headers():
    user_agent_use = config.user_agent[random.randint(0, len(config.user_agent) - 1)]
    headers_use = {
        'User-Agent': user_agent_use,
        'Accept': 'application/json, text/plain, */*',
        "cookie": config.cookie.encode("utf-8").decode("latin1")
    }
    return headers_use

def init():
    config.TimeSleep=int(input('[*] 请输入爬取每一页等待的秒数，防止IP被ban\n'))
    config.SearchKEY = input('[*] 请输入fofa搜索关键字 \n')
    return

def get_page_num(search_key):
    headers_use = headers()
    searchbs64 = quote_plus(base64.b64encode(search_key.encode()))
    print("[*] 爬取页面为:https://fofa.info/result?qbase64=" + searchbs64)
    html = requests.get(url="https://fofa.info/result?qbase64=" + searchbs64, headers=headers_use).text
    tree = etree.HTML(html)
    try:
        pagenum = tree.xpath('//li[@class="number"]/text()')[-1]
    except Exception as e:
        print(e)
        pagenum = '0'
        pass
    print("[*] 存在页码:"+pagenum)
    return searchbs64, headers_use

def getTimeList(text):
    timelist=list()
    pattern="<span>[0-9]*-[0-9]*-[0-9]*</span>"
    result = re.findall(pattern, text)
    for temp in result:
        timelist.append(temp.replace("<span>","").replace("</span>","").strip())
    # print(timelist)
    return timelist

def fofa_spider_page(page, search_key, searchbs64, headers_use, turn_num):
    global host_list
    global timestamp_list
    searchurl = quote_plus(search_key)# searchurl是search_key url encode
    searchurl = searchurl.replace('%28', '(').replace('%29', ')')
    print("[*] 正在爬取第" + str(5*int(turn_num) + int(page)) + "页")
    request_url = 'https://fofa.info/result?qbase64=' + searchbs64 + '&full=false&page=' + str(page) +"&page_size=10"
    # print('request_url:')
    # print(request_url)
    rep = requests.get(request_url, headers=headers_use)
    tree = etree.HTML(rep.text)
    urllist = tree.xpath('//span[@class="aSpan"]/a/@href')
    timelist=getTimeList(rep.text)
    print(urllist)
    host_list.extend(urllist)
    timestamp_list.extend(timelist)

    time.sleep(config.TimeSleep)
    return


def fofa_spider(search_key, searchbs64, headers_use):
    global host_list

    start_page = input("[*] 请输入开始页码: ")
    want_page = input("[*] 请输入终止页码: ")
    if int(want_page) <= 5 and int(want_page) > 0:
        stop_page = want_page
        for page in range(int(start_page), int(stop_page) + 1):
            fofa_spider_page(page, search_key, searchbs64, headers_use, turn_num=0)
    elif int(want_page) > 5:
        if int(want_page) % 5 == 0:
            start_page = start_page
            stop_page = 5
            for turn_num in range(int(int(want_page) / 5)):

                global timestamp_list
                # print('[*] 第 ' + str(turn_num + 1) + ' turn抓取')
                timestamp_list.clear()
                for page in range(int(start_page), int(stop_page) + 1):
                    fofa_spider_page(page, search_key, searchbs64, headers_use, turn_num)

                search_key_modify, searchbs64_modify = modify_search_url(search_key)
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
                    fofa_spider_page(page, search_key, searchbs64, headers_use, turn_num)

                search_key_modify, searchbs64_modify = modify_search_url(search_key)
                search_key = search_key_modify
                searchbs64 = searchbs64_modify
            for page in range(1, page_last + 1):
                # print('[*] 第 ' + str(turn_num + 2) + ' turn抓取')
                fofa_spider_page(page, search_key, searchbs64, headers_use, turn_num=turn_sum)
    else:
        print('[-] 输入错误')
        exit(0)
    return

def modify_search_url(search_key):
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

def host_list_print():
    global host_list
    print("="*60+'\n')
    doc_result = open('spider_result.txt', 'w+')
    for host in host_list:
        print('[+] ' + host)
        doc_result.write(host + '\n')
    doc_result.close()
    print('[+] 抓取结束，共抓取数据 ' + str(len(host_list)) + ' 条\n')
    return

def main():
    logo()
    checkSession()
    init()
    searchbs64, headers_use = get_page_num(config.SearchKEY)
    fofa_spider(config.SearchKEY, searchbs64, headers_use)
    host_list_print()

def test():
    print('hi')


if __name__ == '__main__':
    main()
