"""
   File Name :    test.py
   Description :
   Author :       Cl0udG0d
   date :         2023/2/12
"""
import datetime
import json
import time

import requests
from lxml import etree

def cleanData(urllist):
    newlist=list()
    for url in urllist:
        newlist.append(url.strip())
    return newlist

resp = requests.get(url='https://fofa.info/result?qbase64=MQ==&page_size=10')
tree = etree.HTML(resp.text)
urllist1 = tree.xpath('//span[@class="hsxa-host"]/text()')

urllist2 = tree.xpath('//span[@class="hsxa-host"]/a/@href')

print(cleanData(urllist1)+urllist2)
