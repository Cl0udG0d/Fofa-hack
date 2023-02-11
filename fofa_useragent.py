"""
   File Name :    fofa_useragent.py
   Description :
   Author :       Cl0udG0d
   date :         2023/2/12
"""
import config
import random

def getFakeUserAgent():
    """
    获取一个随机伪造的useragent
    :return:
    """
    return config.user_agent[random.randint(0, len(config.user_agent) - 1)]

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
        'Referer': 'https://i.nosec.org/login?service=https://fofa.info/f_login',
        'Host': 'i.nosec.org',
        'Origin': 'https://i.nosec.org',
        'sec-ch-ua': '"Chromium";v="106", "Microsoft Edge";v="106", "Not;A=Brand";v="99"',
        'sec-ch-ua-platform': '"Windows"',
    }
    return headers

def getCheckHeaders(cookies):
    """
    该headers检测cookies是否有效
    :param cookies:
    :return:
    """
    check_headers = {
        'Host': 'fofa.info',
        'User-Agent': getFakeUserAgent(),
        'sec-ch-ua': '"Chromium";v="106", "Microsoft Edge";v="106", "Not;A=Brand";v="99"',
        'sec-ch-ua-platform': '"Windows"',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'DNT': '1',
        'Referer': 'https://fofa.info/',
        'Connection': 'keep-alive',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Cookie': cookies,
    }
    return check_headers