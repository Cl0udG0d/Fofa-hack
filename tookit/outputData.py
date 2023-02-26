import json


class OutputData:

    '''
    常量
    '''
    CONST_TXT = "txt"
    CONST_JSON = "json"
    CONST_CSV = "csv"
    STANDARD_LIST = [CONST_TXT, CONST_JSON, CONST_CSV]

    ENCODING_TYPE="utf-8"

    def __init__(self,filename,pattern="txt"):
        self.filename=filename
        self.pattern = pattern if self.checkPatternStandard(pattern) else "txt"


    def checkPatternStandard(self, pattern):
        """
        检测pattern是否合规
        :param pattern:
        :return:
        """
        return pattern in self.STANDARD_LIST

    def output(self,data):
        self.filename="{}.{}".format(self.filename,self.pattern)
        if self.pattern==self.CONST_TXT:
            self.outputTxt(data)
        elif self.pattern==self.CONST_JSON:
            pass
        else:
            pass

    def outputTxt(self,data):
        for i in data:
            with open(self.filename, 'a+', encoding=self.ENCODING_TYPE) as f:
                f.write(str(i) + "\n")


    def readAllJsonData(self):
        with open("../{}".format(self.filename), 'r+', encoding=self.ENCODING_TYPE) as load_f:
            load_dict = json.load(load_f)
            print(load_dict)
        return

    def outputJson(self,newdata):
        listdata=self.readAllJsonData()
        if type(listdata) != list:
            listdata = []
        for data in newdata:
            listdata.append(data)
        with open(self.filename, 'w', encoding=self.ENCODING_TYPE) as f:
            json.dump(listdata, f)

    def outputCsv(self):
        return
