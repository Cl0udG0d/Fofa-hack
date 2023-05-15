"""
   File Name :    test.py
   Description :
   Author :       Cl0udG0d
   date :         2023/2/12
"""
from tookit.outputData import OutputData

if (1 == 1):
    print(1)
output = OutputData("123", "json")
output.outputJson(["123", "456", "789"])
