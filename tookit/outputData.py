import csv
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

    ENCODING_TYPE = "utf-8"

    def __init__(self, filename, level="1", pattern="txt"):
        self.filename = filename
        # self.outputname=outputname
        self.pattern = pattern if self.checkPatternStandard(pattern) else "txt"
        self.level = level
        self.header_written = False
        # self.path=os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))),self.filename)


    def checkPatternStandard(self, pattern):
        """
        检测pattern是否合规
        :param pattern:
        :return:
        """
        return pattern in self.STANDARD_LIST

    def output(self, data):
        # self.filename="{}.{}".format(self.filename,self.pattern)
        if self.pattern == self.CONST_TXT:
            self.outputTxt(data)
        elif self.pattern == self.CONST_JSON:
            self.outputJson(data)
        elif self.pattern == self.CONST_CSV:
            self.outputCsv(data)
        else:
            pass

    def outputTxt(self, data):
        with open(self.filename, 'a+', encoding=self.ENCODING_TYPE) as f:
            for i in data:
                f.write(str(i) + "\n")

    def readAllJsonData(self):
        # print(os.path.exists(self.filename))
        if os.path.exists(self.filename) == False or os.path.getsize(self.filename) == 0:
            return {}
        else:
            with open(self.filename, 'r+', encoding=self.ENCODING_TYPE) as load_f:
                if load_f:
                    load_dict = json.load(load_f)
                    return load_dict
        return {}

    def outputJson(self, newdata):
        data = self.readAllJsonData()

        with open(self.filename, 'w+', encoding=self.ENCODING_TYPE) as load_f:

            for i in newdata:
                if self.level == "1":
                    data[i] = i
                elif self.level == "2":
                    keyword = i["url"]
                    data[keyword] = {}
                    data[keyword]["url"] = i["url"]
                    data[keyword]["port"] = i["port"]
                    data[keyword]["title"] = i["title"]
                    data[keyword]["ip"] = i["ip"]
                else:
                    keyword = i["link"]
                    data[keyword] = i

            json.dump(data, load_f, indent=4, ensure_ascii=False)
            load_f.close()
        # print(os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))),self.filename))
        # with open(self.path, 'w+', encoding=self.ENCODING_TYPE) as r:
        #
        # r.close()

    def getCsvHeaders(self, data):
        headers = []
        if len(data)>0:
            if type(data[0]) is dict:

                headers = list(data[0].keys())
            else:
                headers = ["link"]
        return headers

    def outputCsv(self, data):
        headers = self.getCsvHeaders(data)
        with open('score.csv', mode='a+', newline='', encoding='utf-8-sig') as file:
            writer = csv.writer(file)

            # 如果尚未写入表头，则写入表头
            if not self.header_written:
                writer.writerow(headers)
                self.header_written = True

            for i in data:
                if self.level == "1":
                    writer.writerow([i])
                elif self.level == "2" or self.level == "3":
                    writer.writerow(list(i.values()))




if __name__ == '__main__':
    output = OutputData("123", "json")
    output.outputJson(["123", "456", "789"])
