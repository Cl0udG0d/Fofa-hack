#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/9/24 22:28
# @Author  : Cl0udG0d
# @File    : sign.py
# @Github: https://github.com/Cl0udG0d
from Cryptodome.Signature import PKCS1_v1_5
from Cryptodome.Hash import SHA256
from Cryptodome.PublicKey import RSA
import urllib.parse
import time
import base64

from tookit import config

'''
加密算法部分感谢 tastypear
'''

private_key_str = '''-----BEGIN RSA PRIVATE KEY-----
MIIEogIBAAKCAQEAv0xjefuBTF6Ox940ZqLLUFFBDtTcB9dAfDjWgyZ2A55K+VdG
c1L5LqJWuyRkhYGFTlI4K5hRiExvjXuwIEed1norp5cKdeTLJwmvPyFgaEh7Ow19
Tu9sTR5hHxThjT8ieArB2kNAdp8Xoo7O8KihmBmtbJ1umRv2XxG+mm2ByPZFlTdW
RFU38oCPkGKlrl/RzOJKRYMv10s1MWBPY6oYkRiOX/EsAUVae6zKRqNR2Q4HzJV8
gOYMPvqkau8hwN8i6r0z0jkDGCRJSW9djWk3Byi3R2oSdZ0IoS+91MFtKvWYdnNH
2Ubhlnu1P+wbeuIFdp2u7ZQOtgPX0mtQ263e5QIDAQABAoIBAD67GwfeTMkxXNr3
5/EcQ1XEP3RQoxLDKHdT4CxDyYFoQCfB0e1xcRs0ywI1be1FyuQjHB5Xpazve8lG
nTwIoB68E2KyqhB9BY14pIosNMQduKNlygi/hKFJbAnYPBqocHIy/NzJHvOHOiXp
dL0AX3VUPkWW3rTAsar9U6aqcFvorMJQ2NPjijcXA0p1MlZAZKODO2wqidfQ487h
xy0ZkriYVi419j83a1cCK0QocXiUUeQM6zRNgQv7LCmrFo2X4JEzlujEveqvsDC4
MBRgkK2lNH+AFuRwOEr4PIlk9rrpHA4O1V13P3hJpH5gxs5oLLM1CWWG9YWLL44G
zD9Tm8ECgYEA8NStMXyAmHLYmd2h0u5jpNGbegf96z9s/RnCVbNHmIqh/pbXizcv
mMeLR7a0BLs9eiCpjNf9hob/JCJTms6SmqJ5NyRMJtZghF6YJuCSO1MTxkI/6RUw
mrygQTiF8RyVUlEoNJyhZCVWqCYjctAisEDaBRnUTpNn0mLvEXgf1pUCgYEAy1kE
d0YqGh/z4c/D09crQMrR/lvTOD+LRMf9lH+SkScT0GzdNIT5yuscRwKsnE6SpC5G
ySJFVhCnCBsQqq+ohsrXt8a99G7ePTMSAGK3QtC7QS3liDmvPBk6mJiLrKiRAZos
vgPg7nTP8VuF0ZIKzkdWbGoMyNxVFZXovQ8BYxECgYBvCR9xGX4Qy6KiDlV18wNu
ElYkxVqFBBE0AJRg/u+bnQ9jWhi2zxLa1eWZgtss80c876I8lbkGNWedOVZioatm
MFLC4bFalqyZWyO7iP7i60LKvfDJfkOSlDUu3OikahFOiqyG1VBz4+M4U500alIU
AVKD14zTTZMopQSkgUXsoQKBgHd8RgiD3Qde0SJVv97BZzP6OWw5rqI1jHMNBK72
SzwpdxYYcd6DaHfYsNP0+VIbRUVdv9A95/oLbOpxZNi2wNL7a8gb6tAvOT1Cvggl
+UM0fWNuQZpLMvGgbXLu59u7bQFBA5tfkhLr5qgOvFIJe3n8JwcrRXndJc26OXil
0Y3RAoGAJOqYN2CD4vOs6CHdnQvyn7ICc41ila/H49fjsiJ70RUD1aD8nYuosOnj
wbG6+eWekyLZ1RVEw3eRF+aMOEFNaK6xKjXGMhuWj3A9xVw9Fauv8a2KBU42Vmcd
t4HRyaBPCQQsIoErdChZj8g7DdxWheuiKoN4gbfK4W1APCcuhUA=
-----END RSA PRIVATE KEY-----'''


def getSign(message):
    priv_key = RSA.importKey(private_key_str)
    h = SHA256.new(message.encode('utf-8'))
    signature = PKCS1_v1_5.new(priv_key).sign(h)
    result = base64.b64encode(signature).decode()
    return result


def getUrl(qbase64):
    ts = int(time.time() * 1000)
    size = 50 if config.AUTHORIZATION else 20
    message = f'fullfalsepage1qbase64{qbase64}size{size}ts{ts}'
    sign = urllib.parse.quote(getSign(message))
    url = f'https://api.fofa.info/v1/search?qbase64={urllib.parse.quote(qbase64)}&full=false&page=1&size={size}&ts={ts}&sign={sign}&app_id=9e9fb94330d97833acfbc041ee1a76793f1bc691'
    return url

# def getPage2Url(qbase64,page):
#     ts = int(time.time() * 1000)
#     message = f'fullfalsepage{page}qbase64{qbase64}size10ts{ts}'
#     sign = urllib.parse.quote(getSign(message))
#     url = f'https://api.fofa.info/v1/search?qbase64={urllib.parse.quote(qbase64)}&full=false&page={page}&size=10&ts={ts}&sign={sign}&app_id=9e9fb94330d97833acfbc041ee1a76793f1bc691'
#     return url

def getUrlTest(qbase64):
    ts = int(time.time() * 1000)
    size = 10 if config.AUTHORIZATION else 20
    message = f'fullfalsepage1qbase64{qbase64}size{size}ts{ts}'
    sign = urllib.parse.quote(getSign(message))
    url = f'https://api.fofa.info/v1/search?qbase64={urllib.parse.quote(qbase64)}&full=false&page=1&size={size}&ts={ts}&sign={sign}&app_id=9e9fb94330d97833acfbc041ee1a76793f1bc691'
    return url


if __name__ == '__main__':
    print(getUrlTest("aWNvbl9oYXNoPSIxMzMxOTQ0ODc3Ig=="))
