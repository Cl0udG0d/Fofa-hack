"""
   File Name :    bypass.py
   Description :
   Author :       Cl0udG0d
   date :         2023/3/1
"""
import base64
import re

from lxml import etree


class ByPass:

    '''
    爬取规则
    '''
    LEFT_LIST_RULE = '//div[@class="hsxa-meta-data-list-main-left hsxa-fl"]'
    CITY_RULE = 'p[3]/a/@href'

    CITY_SET=set()

    def __init__(self,context):
        self.context=context
        self.tree = etree.HTML(context)
        self.leftList = self.tree.xpath(self.LEFT_LIST_RULE)
        self.filterDict={
            "country":[]
        }

    def fuzzMain(self):
        return


    def switchBypass(self,key):
        if key=="country":
            return self.bypassCountry()
        elif key=="port":
            return self.bypassPort()
        elif key=="server":
            return self.bypassServer()
        elif key=="protocol":
            return self.bypassProtocol()
        elif key=="title":
            return self.bypassTitle()
        else:
            return list()

    def filterKeyword(self):
        return

    def bypassProtocol(self):
        return

    def bypassCountry(self):
        countryList=list()
        for i in range(len(self.leftList)):
            cityURL = self.tree.xpath(self.CITY_RULE)[0].strip()
            city=self.filterKeyword(cityURL,"country")
            if city not in self.CITY_SET:
                self.CITY_SET.add(city)
                countryList.append(city)
        return countryList

    def filterKeyword(self,keyURL,key):
        searchbs64=keyURL.split("qbase64=")[1]
        search_key=base64.b64decode(searchbs64)
        if key in search_key:
            pattern = r'{}="([^"]+)"'.format(key)
            match = re.search(pattern, search_key)
            city = match.group(1)
            return city


    def bypassCity(self):
        return

    def bypassAsn(self):
        return 

    def bypassPort(self):
        return

    def bypassJs(self):
        return

    def bypassServer(self):
        return

    def bypassStatusCode(self):
        return

    def bypassBody(self):
        return

    def bypassTitle(self):
        return

    def bypassTime(self):
        return

    def bypassOs(self):
        return


