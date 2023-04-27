import json
import os


class OutputData:

    '''
    常量
    '''
    CONST_TXT = "txt"
    CONST_JSON = "json"
    CONST_CSV = "csv"
    STANDARD_LIST = [CONST_TXT, CONST_JSON, CONST_CSV]

    ENCODING_TYPE="utf-8"

    def __init__(self,filename,level="1",pattern="txt"):
        self.filename=filename
        self.pattern = pattern if self.checkPatternStandard(pattern) else "txt"
        self.level=level
        # self.path=os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))),self.filename)

    def initFile(self):

        return

    def checkPatternStandard(self, pattern):
        """
        检测pattern是否合规
        :param pattern:
        :return:
        """
        return pattern in self.STANDARD_LIST

    def output(self,data):
        # self.filename="{}.{}".format(self.filename,self.pattern)
        if self.pattern==self.CONST_TXT:
            self.outputTxt(data)
        elif self.pattern==self.CONST_JSON:
            self.outputJson(data)
        else:
            pass

    def outputTxt(self,data):
        with open(self.filename, 'a+', encoding=self.ENCODING_TYPE) as f:
            for i in data:
                f.write(str(i) + "\n")


    def readAllJsonData(self):
        # print(os.path.exists(self.filename))
        if os.path.exists(self.filename)==False or os.path.getsize(self.filename)==0:
            return {}
        else:
            with open(self.filename, 'r+', encoding=self.ENCODING_TYPE) as load_f:
                if load_f:
                    load_dict = json.load(load_f)
                    return load_dict
        return {}

    def outputJson(self,newdata):
        data=self.readAllJsonData()

        with open(self.filename, 'w+', encoding=self.ENCODING_TYPE) as load_f:
            # load_f.seek(0)
            # print(os.path.getsize(self.filename))
            # print("lines : " + str(load_f.readlines()))
            # if os.path.getsize(self.filename)==0:
            #     load_dict={}
            # else:
            #     print("lines : "+str(load_f.readlines()))
            #     load_dict = json.load(load_f)
            # print(load_dict)

            for i in newdata:
                if self.level=="1":
                    data[i] = i
                elif self.level=="2":
                    data[i] = {}
                    data[i]["url"] = i["url"]
                    data[i]["port"] = i["port"]
                    data[i]["title"] = i["title"]
                    data[i]["ip"] = i["ip"]
                else :
                    data[i] = {}
                    data[i]["url"] = i["url"]
                    data[i]["port"] = i["port"]
                    data[i]["title"] = i["title"]
                    data[i]["ip"] = i["ip"]
                    data[i]["city"] = i["city"]
                    data[i]["asn"] = i["asn"]
                    data[i]["organization"] = i["organization"]
                    data[i]["server"] = i["server"]
                    data[i]["rep"] = i["rep"]
            print(data)

            json.dump(data, load_f, indent=4, ensure_ascii=False)
            load_f.close()
        # print(os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))),self.filename))
        # with open(self.path, 'w+', encoding=self.ENCODING_TYPE) as r:
        #
        # r.close()

    def outputCsv(self):
        return

if __name__ == '__main__':
    output = OutputData("123", "json")
    output.outputJson(["123", "456", "789"])
