import hashlib
import random
import string
import time

from tookit import config


def md5(str):
    m = hashlib.md5()
    m.update(str.encode("utf8"))
    # print(m.hexdigest())
    return m.hexdigest()

def get_username():
    return generate_username(5)

def generate_username(length):
    letters = string.ascii_lowercase
    random_str=''.join(random.choice(letters) for i in range(length))
    return random_str+"_"+str(int(time.time()))

def outputLogo():
    print('''\033[1;32m
             ____  ____  ____  ____      
            | ===|/ () \| ===|/ () \     
            |__|  \____/|__| /__/\__\    
                 _   _   ____   ____  __  __ 
                | |_| | / () \ / (__`|  |/  /
                |_| |_|/__/\__\\\\____)|__|\__\\ \033[0m\033[1;34mV{}\033[0m

                \033[1;32m公众号: 黑糖安全\033[0m
            '''.format(config.VERSION_NUM))

def clipKeyWord(keyword):
    """
    修剪查找关键字
    @param keyword:
    @return:
    """
    tempkey = keyword.replace("'", '"')
    # print(tempkey)

    if '"' not in tempkey and ' ' not in tempkey:
        if "=" in tempkey:
            # print("=".join(tempkey.split("=")[1:]))
            tempkey = tempkey.split("=")[0] + '="' + "=".join(tempkey.split("=")[1:]) + '"'
        else:
            tempkey = '"{}"'.format(tempkey)
    return tempkey

def setProxy(proxy):
    """
    设置代理
    """
    proxies = {}
    if proxy:
        proxies = {
            'http': 'http://' + proxy,
            'https': 'http://' + proxy
        }
        is_proxy = True
        return is_proxy, proxies
    else:
        is_proxy = False
        return is_proxy,proxies
