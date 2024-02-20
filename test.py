import requests

from fofa_hack import fofa
from tookit import fofaUseragent

from tookit.sign import getUrl, getPage2Url


def main():
    target_url = getPage2Url("ImhpIg==",10)
    print(target_url)
    html = requests.get(url=target_url,
                        headers=fofaUseragent.getFofaCookieHeaders(), timeout=5) \
        .text
    print(html)
    # result_generator = fofa.api('body="亿邮邮件" && country="CN" && region!="HK" && region!="MO"', endcount=100)
    # for data in result_generator:
    #     print(data)

if __name__ == '__main__':
    main()