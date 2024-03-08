import requests

from fofa_hack import fofa
from tookit import fofaUseragent

import requests,sys,mmh3,codecs

def main():
    # result_generator = fofa.api('body="亿邮邮件" && country="CN" && region!="HK" && region!="MO"', endcount=100)
    # for data in result_generator:
    #     print(data)
    import mmh3
    import requests
    import base64
    # f = open("favicon32.ico","rb")
    filename = "favicon32.ico"
    # print(f.read())
    with open(filename, 'rb') as f:
        _icon = mmh3.hash(codecs.lookup('base64').encode(f.read())[0])
        print('http.favicon.hash:' + str(_icon))


    # response = requests.get('https://g.csdnimg.cn/static/logo/favicon32.ico')
    # favicon = base64.b64encode(response.content)
    # hash = mmh3.hash(favicon)


if __name__ == '__main__':
    main()