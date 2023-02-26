'''
    levelData 根据不同level爬取对应的结果
'''
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
    TITLE_RULE='//p[@class="hsxa-two-line"]/text()'
    IP_RULE="p[2]/a/text()"
    CITY_RULE='p[3]/a/text()'
    ASN_RULE='p[4]/a/text()'
    ORGANIZATION_RULE='p[5]/a/text()'
    SERVER_RULE='p[@class="hsxa-list-span-wrap"]/a/span/text()'
    PORTLIST_RULE='//a[@class="hsxa-port"]/text()'
    REP_RULE='//div[@class="el-scrollbar__view"]/span/text()'

    LEFT_LIST_RULE='//div[@class="hsxa-meta-data-list-main-left hsxa-fl"]'
    RIGHT_LIST_RULE='//div[@class="hsxa-meta-data-list-main-right hsxa-fr"]'

    '''
    内部变量
    '''
    level = "1"
    tree = None
    rep = None
    formatData = []

    def __init__(self, level="1"):

        self.level = level if self.checkLevelStandard(level) else "1"
        print("[*] LEVEL = {} , 初始化成功".format(self.level))

        return

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
        self.formatData=[]
        self.rep = rep
        self.tree = etree.HTML(rep.text)
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
        urllist = self.tree.xpath(self.URLLIST_RULE)
        self.formatData = urllist

    def spiderMiddleData(self):
        """
        爬取 level =2 时的数据
            url
            port
            title
            ip
        :return:
        """
        urllist = self.tree.xpath(self.URLLIST_RULE)
        portlist=self.tree.xpath(self.PORTLIST_RULE)
        leftList=self.tree.xpath(self.LEFT_LIST_RULE)
        titleList=self.tree.xpath(self.TITLE_RULE)
        for i in range(len(urllist)):
            tempDic = {}
            tempDic["url"] = urllist[i].strip()
            tempDic["port"]=portlist[i].strip()
            ip = leftList[i].xpath(self.IP_RULE)
            tempDic["title"]=titleList[i].strip()
            tempDic["ip"] = ip[0].strip()
            self.formatData.append(tempDic)

    def stripList(self,data):
        newData = []
        for i in data:
            newData.append(i.strip())
        return newData

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
        urllist = self.tree.xpath(self.URLLIST_RULE)
        portlist = self.tree.xpath(self.PORTLIST_RULE)
        leftList = self.tree.xpath(self.LEFT_LIST_RULE)
        rightList = self.tree.xpath(self.RIGHT_LIST_RULE)
        titleList = self.tree.xpath(self.TITLE_RULE)

        for i in range(len(urllist)):
            tempDic = {}
            ip = leftList[i].xpath(self.IP_RULE)
            city = leftList[i].xpath(self.CITY_RULE)
            asn = leftList[i].xpath(self.ASN_RULE)
            organization = leftList[i].xpath(self.ORGANIZATION_RULE)
            server = leftList[i].xpath(self.SERVER_RULE)
            rep = rightList[i].xpath(self.REP_RULE)

            tempDic["url"] = urllist[i].strip()
            tempDic["port"] = portlist[i].strip()
            tempDic["title"] = titleList[i].strip()
            tempDic["ip"] = ip[0].strip()

            tempDic["city"] = city[0].strip()
            tempDic["asn"] = asn[0].strip()
            tempDic["organization"] = organization[0].strip()
            tempDic["server"] = self.stripList(server)
            tempDic["rep"] = rep[0].strip()
            self.formatData.append(tempDic)



