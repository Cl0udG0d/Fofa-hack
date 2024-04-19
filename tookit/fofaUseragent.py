"""
   File Name :    fofaUseragent.py
   Description :
   Author :       Cl0udG0d
   date :         2023/2/12
"""
import random

from tookit import config

user_agent = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3100.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
    'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
    'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11',
    'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
]

def getFakeUserAgent():
    """
    获取一个随机伪造的useragent
    :return:
    """
    return user_agent[random.randint(0, len(user_agent) - 1)]

def getFofaCaptchaHeaders():
    """
    获取fofa验证码网址请求头
    :return:
    """
    fofa_headers = {
        'User-Agent': getFakeUserAgent(),
        'Host': 'i.nosec.org',
        'Referer': 'https://i.nosec.org/login',
        'sec-ch-ua': '"Chromium";v="106", "Microsoft Edge";v="106", "Not;A=Brand";v="99"',
        'sec-ch-ua-platform': '"Windows"',
    }
    return fofa_headers

def getFofaLoginHeaders():
    """
    获取fofa登录网址headers
    :return:
    """
    headers = {
        'User-Agent': getFakeUserAgent(),
        'Referer': 'https://i.nosec.org/login?service=https://octra.fofa.vip/fofaLogin',
        'Host': 'i.nosec.org',
        'Origin': 'https://i.nosec.org',
        'sec-ch-ua': '"Chromium";v="106", "Microsoft Edge";v="106", "Not;A=Brand";v="99"',
        'sec-ch-ua-platform': '"Windows"',
    }
    return headers

def getCheckHeaders():
    """
    该headers检测cookies是否有效
    :param cookies:
    :return:
    """
    check_headers = {
        'Host': 'fofa_hack.info',
        'User-Agent': getFakeUserAgent(),
        'sec-ch-ua': '"Chromium";v="106", "Microsoft Edge";v="106", "Not;A=Brand";v="99"',
        'sec-ch-ua-platform': '"Windows"',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'DNT': '1',
        'Referer': 'https://fofa.info/',
        'Connection': 'keep-alive',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    }
    return check_headers


def getFofaPageNumHeaders():
    headers_use = {
        'User-Agent': getFakeUserAgent(),
        'Accept': 'application/json, text/plain, */*',
    }
    if config.AUTHORIZATION:
        headers_use['Authorization'] = config.AUTHORIZATION
    return headers_use


def getNormalHeaders():
    headers_use = {
        'User-Agent': getFakeUserAgent(),
        'Accept': 'application/json, text/plain, */*',
    }
    return headers_use

# def getFofaCookieHeaders():
#     headers_use = {
#         'User-Agent': getFakeUserAgent(),
#         'Accept': 'application/json, text/plain, */*',
#         'Authorization':config.AUTHORIZATION,
#     }
#     return headers_use