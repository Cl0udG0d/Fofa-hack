"""
   File Name :    test.py
   Description :
   Author :       Cl0udG0d
   date :         2023/2/12
"""
import datetime
import time

import requests
from lxml import etree
def stripList(data):
    newData=[]
    for i in data:
        newData.append(i.strip())
    return newData
request_url = "https://fofa.info/result?qbase64=dGhpbmtwaHA%3D"
rep = requests.get(request_url)
tree = etree.HTML(rep.text)
leftList = tree.xpath('//div[@class="hsxa-meta-data-list-main-left hsxa-fl"]')

print(leftList)
for i in range(len(leftList)):
    title=leftList[i].xpath('p[@class="hsxa-two-line"]/text()')
    ip=leftList[i].xpath('p[2]/a/text()')
    city=leftList[i].xpath('p[3]/a/text()')
    asn = leftList[i].xpath('p[4]/a/text()')
    organization=leftList[i].xpath('p[5]/a/text()')
    server=leftList[i].xpath('p[@class="hsxa-list-span-wrap"]/a/span/text()')
    print("title: "+str(title[0].strip()))
    print("ip: "+ip[0].strip())
    print("city: " + city[0].strip())
    print("asn: " + asn[0].strip())
    print("organization: " + organization[0].strip())
    print("server: " + str(stripList(server)))


rightList=tree.xpath('//div[@class="hsxa-meta-data-list-main-right hsxa-fr"]')
for i in range(len(rightList)):
    rep=rightList[i].xpath('//div[@class="el-scrollbar__view"]/span/text()')
    print(rep[0].strip())

portlist=tree.xpath('//div[@class="hsxa-fr"]/a/text()')
for i in portlist:
    print(i.strip())