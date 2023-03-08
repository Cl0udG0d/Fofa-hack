"""
   File Name :    test.py
   Description :
   Author :       Cl0udG0d
   date :         2023/2/12
"""
import datetime
import json
import time

import requests
from lxml import etree

data=[1,2,3,4,5,6,7,8,9]
result=[]



for i in data:

    for j in data:
        for k in data:
            for l in data:
                for m in data:
                    for n in data:
                        num1=i*10+j
                        num2=k
                        num3=l*10+m
                        num4=n
                        if num1-num2==num3-num4:
                            templist=[i,j,k,l,m,n]
                            if templist.count(2)<2 and templist.count(3)<2 and templist.count(4)<2 and templist.count(5)<2 and templist.count(6)<2 and templist.count(7)<2 and templist.count(8)<2 and templist.count(9)<2:

                                print("{}-{}={}-{}".format(num1,num2,num3,num4))
                                result.append([num1,num2,num3,num4])

print(len(result))