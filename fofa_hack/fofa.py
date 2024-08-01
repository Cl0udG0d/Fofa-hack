#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/12/15 17:37
# @Author  : Cl0udG0d
# @File    : fofa.py
# @Github: https://github.com/Cl0udG0d
import base64
import json
import re
import time
from datetime import datetime
from datetime import timedelta
import requests

from tookit import fofaUseragent
from tookit.sign import getUrl


def get_timestamp_list(text):
    timelist = list()
    data = json.loads(text)
    assets = data["data"]["assets"]
    for asset in assets:
        mtime = asset["mtime"].split()[0]
        timelist.append(mtime)
    return timelist


def get_searchkey(search_key, timelist):
    before_time_in_search_key = (datetime.today() + timedelta(days=1)).strftime('%Y-%m-%d')
    if "before=" in search_key:
        pattern = r'before="([^"]+)"'
        match = re.search(pattern, search_key)
        before_time_in_search_key = match.group(1)
    time_before_time_in_search_key = datetime.strptime(before_time_in_search_key, "%Y-%m-%d").date()

    timestamp_list = list(timelist)
    timestamp_list.sort()
    if len(timestamp_list) == 0:
        return search_key

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

    return search_key_modify


def base64_api(search_basekey, endcount=100, timesleep=3, timeout=180, proxy=None):
    host_set = set()
    last_num = 0
    fofa_key = base64.b64decode(search_basekey).decode('utf-8')
    while len(host_set) < endcount or (last_num != 0 and last_num == len(host_set)):
        print(fofa_key)
        time.sleep(timesleep)
        searchbs64 = base64.b64encode(f'{fofa_key}'.encode()).decode()
        request_url = getUrl(searchbs64)
        rep = requests.get(request_url, headers=fofaUseragent.getFofaPageNumHeaders(), timeout=timeout,
                           proxies=proxy)
        timelist = get_timestamp_list(rep.text)
        data = json.loads(rep.text)
        format_data = [d['link'] if d['link'] != '' else d['host'] for d in data["data"]["assets"]]
        fofa_key = get_searchkey(fofa_key, timelist)
        last_num += len(host_set)
        for url in format_data:
            host_set.add(url)
        yield format_data


def api(search_key, endcount=100, timesleep=3, timeout=180, proxy=None):
    host_set = set()
    last_num = 0
    fofa_key = search_key
    while len(host_set) < endcount or (last_num != 0 and last_num == len(host_set)):
        # print(fofa_key)
        time.sleep(timesleep)
        searchbs64 = base64.b64encode(f'{fofa_key}'.encode()).decode()
        request_url = getUrl(searchbs64)
        rep = requests.get(request_url, headers=fofaUseragent.getFofaPageNumHeaders(), timeout=timeout,
                           proxies=proxy)
        # request should be success
        rep.raise_for_status()
        # request should not be limited
        # '{"code":820006,"message":"[820006] 资源访问每天限制","data":""}'
        if len(rep.text) <= 55 and '820006' in rep.text:
            raise RuntimeError("API call limit reached for today,call at next day or use proxy")
        timelist = get_timestamp_list(rep.text)
        data = json.loads(rep.text)
        format_data = [d['link'] if d['link'] != '' else d['host'] for d in data["data"]["assets"]]
        fofa_key = get_searchkey(fofa_key, timelist)
        last_num += len(host_set)
        for url in format_data:
            host_set.add(url)
        yield format_data


if __name__ == '__main__':
    result_generator = api("thinkphp", endcount=100)
    for data in result_generator:
        print(data)
