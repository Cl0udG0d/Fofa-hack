"""
   File Name :    test.py
   Description :
   Author :       Cl0udG0d
   date :         2023/2/12
"""
import datetime
import json
import time


def outputJson(data):

    with open("test.json", 'w', encoding="utf-8") as f:
        dic={"1":"2"}
        data.append(dic)
        json.dump(data, f)

def readAllJsonData():
    with open("test.json", 'r',encoding="utf-8") as load_f:
        load_dict = json.load(load_f)
        print(type(load_dict))
        print(load_dict)
    return

data=[
    {"2":"3"}
]

outputJson(data)

readAllJsonData()