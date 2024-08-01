'''
    levelData 根据不同level爬取对应的结果
'''
import json

from lxml import etree


class LevelData:
    '''
    常量
    '''
    PRIMARYDATA = "1"
    MIDDLEDATA = "2"
    HIGHDATA = "3"
    STANDARD_LIST = [PRIMARYDATA, MIDDLEDATA, HIGHDATA]

    '''
    爬取规则
    '''
    URLLIST_RULE = '//span[@class="hsxa-host"]/a/@href'
    URLLIST_RULE_TWO = '//span[@class="hsxa-host"]/text()'
    TITLE_RULE = '//p[@class="hsxa-two-line"]/text()'
    IP_RULE = "p[2]/a/text()"
    CITY_RULE = 'p[3]/a/text()'
    ASN_RULE = 'p[4]/a/text()'
    ORGANIZATION_RULE = 'p[5]/a/text()'
    SERVER_RULE = 'p[@class="hsxa-list-span-wrap"]/a/span/text()'
    PORTLIST_RULE = '//a[@class="hsxa-port"]/text()'
    REP_RULE = '//div[@class="el-scrollbar__view"]/span/text()'

    LEFT_LIST_RULE = '//div[@class="hsxa-meta-data-list-main-left hsxa-fl"]'
    RIGHT_LIST_RULE = '//div[@class="hsxa-meta-data-list-main-right hsxa-fr"]'

    '''
    内部变量
    '''
    level = "1"
    # tree = None
    rep = None
    format_data = []
    assets=[]

    def __init__(self, level="1"):
        self.level = level if self.checkLevelStandard(level) else "1"

    def checkLevelStandard(self, level):
        """
        检测level是否合规
        :param level:
        :return:
        """
        return level in self.STANDARD_LIST

    def startSpider(self, rep):
        """
        level 1:
            url
        level 2:
            url status
        :param rep:
        :return:
        """
        self.format_data = []
        self.rep = rep
        # self.tree = etree.HTML(rep.text)
        data = json.loads(self.rep.text)
        self.assets=data["data"]["assets"]
        self.selectSpiderRule()

    def selectSpiderRule(self):
        if self.level == self.PRIMARYDATA:
            self.spiderPrimaryData()
        elif self.level == self.MIDDLEDATA:
            self.spiderMiddleData()
        else:
            self.spiderHighData()

    def spiderPrimaryData(self):
        """
        爬取 level = 1 时的数据
            url
        :return:
        """
        # urllist1 = self.tree.xpath(self.URLLIST_RULE)
        # urllist2 = self.cleanUrlListSpeace(self.tree.xpath(self.URLLIST_RULE_TWO))

        self.format_data = [d['link'] if d['link'] != '' else d['host'] for d in self.assets]

    def spiderMiddleData(self):
        """
        爬取 level =2 时的数据
            url
            port
            title
            ip
        :return:
        """
        urllist = [d['link'] if d['link'] != '' else d['host'] for d in self.assets]
        portlist = [d['port'] for d in self.assets]
        titleList = [d['title'] for d in self.assets]
        iplist = [d['ip'] for d in self.assets]
        for i in range(len(urllist)):
            temp_dic = {}
            temp_dic["url"] = urllist[i].strip()
            temp_dic["port"] = portlist[i]
            temp_dic["title"] = titleList[i].strip()
            temp_dic["ip"] = iplist[i].strip()
            self.format_data.append(temp_dic)

    def stripList(self, data):
        new_data = []
        for i in data:
            new_data.append(i.strip())
        return new_data

    def spiderHighData(self):
        """
        爬取 level =3 时的数据
            url
            port
            title
            ip
            city
            asn
            organization
            server
            rep
        :return:
        """
        self.format_data=self.assets
        # urllist1 = self.tree.xpath(self.URLLIST_RULE)
        # urllist2 = self.cleanUrlListSpeace(self.tree.xpath(self.URLLIST_RULE_TWO))
        # urllist = urllist1 + urllist2
        # port_list = self.tree.xpath(self.PORTLIST_RULE)
        # left_list = self.tree.xpath(self.LEFT_LIST_RULE)
        # right_list = self.tree.xpath(self.RIGHT_LIST_RULE)
        # title_list = self.tree.xpath(self.TITLE_RULE)
        #
        # for i in range(len(urllist)):
        #     temp_dic = {}
        #     ip = left_list[i].xpath(self.IP_RULE)
        #     city = left_list[i].xpath(self.CITY_RULE)
        #     asn = left_list[i].xpath(self.ASN_RULE)
        #     organization = left_list[i].xpath(self.ORGANIZATION_RULE)
        #     server = left_list[i].xpath(self.SERVER_RULE)
        #     rep = right_list[i].xpath(self.REP_RULE) if len(right_list) > i else ["None"]
        #
        #     temp_dic["url"] = urllist[i].strip()
        #     temp_dic["port"] = port_list[i].strip()
        #     temp_dic["title"] = title_list[i].strip()
        #     temp_dic["ip"] = ip[0].strip() if len(ip) > 0 else ""
        #     temp_dic["city"] = city[0].strip() if len(city) > 0 else ""
        #     temp_dic["asn"] = asn[0].strip() if len(asn) > 0 else ""
        #     temp_dic["organization"] = organization[0].strip() if len(organization) > 0 else ""
        #     temp_dic["server"] = self.stripList(server)
        #     temp_dic["rep"] = rep[0].strip() if len(rep) > 0 else ""
        #     self.format_data.append(temp_dic)

    def cleanUrlListSpeace(self, data_list):
        new_list = list()
        for data in data_list:
            data = data.strip()
            new_list.append(data)
        return new_list
