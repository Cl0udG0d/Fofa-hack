import hashlib

from tookit import config


def md5(str):
    m = hashlib.md5()
    m.update(str.encode("utf8"))
    # print(m.hexdigest())
    return m.hexdigest()

def outputLogo():
    print('''
             ____  ____  ____  ____      
            | ===|/ () \| ===|/ () \     
            |__|  \____/|__| /__/\__\    
                 _   _   ____   ____  __  __ 
                | |_| | / () \ / (__`|  |/  /
                |_| |_|/__/\__\\\\____)|__|\__\\ V{}

                公众号: 黑糖安全
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
