"""
   File Name :    test.py
   Description :
   Author :       Cl0udG0d
   date :         2023/2/12
"""

import requests

url="https://fofa.info/result?qbase64=InRlc3Qi"
rep=requests.get(url)
print(rep.text)