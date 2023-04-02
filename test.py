"""
   File Name :    test.py
   Description :
   Author :       Cl0udG0d
   date :         2023/2/12
"""
import datetime
import json
import time

# import requests
# from lxml import etree
#
# from tookit.bypass import ByPass
#
# request_url = 'https://fofa.info/result?qbase64=InRoaW5rcGhwIg%3D%3D'
# # print(f'request_url:{request_url}')
# rep = requests.get(request_url,  timeout=5)
# # print(rep.text)
# bypass = ByPass(rep.text)
import click

@click.command()
@click.option('--n', default="aaa")
def dots(n):
    click.echo(n)

if __name__ == '__main__':
    dots()
