# -*- coding: utf-8 -*-
from tookit import config
from tookit.fofa_client import Client
from tookit.unit import colorize


def get_base_results(search_key,size=10000,page=1):
    client = Client(config.FOFA_KEY)
    data = client.search(search_key, size=size, page=page,fields="link,port,protocol,country,region,city,as_number,as_organization,host,domain,os,"
                                "server,product")
    return data["results"]

def get_link_results(search_key,size=10000,page=1):
    client = Client(config.FOFA_KEY)
    data = client.search(search_key, size=size, page=page,
                         fields="link")
    return data["results"]

def get_search_data(search_key,size=10000,page=1):
    client = Client(config.FOFA_KEY)
    data = client.search(search_key, size=size, page=page,
                         fields="")
    return data

def add_city_to_region(result_pool,current_country, current_region, current_city):
    """
    添加城市信息 包含 country region city
    @param result_pool:
    @param current_country:
    @param current_region:
    @param current_city:
    """
    # 检查 current_country 是否存在于 result_pool["country"]
    if current_country not in result_pool["country"]:
        # 如果不存在，则创建它，并初始化为一个空字典
        result_pool["country"][current_country] = {}

        # 检查 current_region 是否存在于 current_country 对应的字典中
    if current_region not in result_pool["country"][current_country]:
        # 如果不存在，则创建它，并初始化为一个空集合
        result_pool["country"][current_country][current_region] = set()

        # 现在可以安全地向 current_region 的集合中添加 current_city
    result_pool["country"][current_country][current_region].add(current_city)


def init_result_pool(results):
    result_pool = {
        "country":{},
        "port":set(),
        "product":set(),
    }
    for result in results:
        current_country = result[3]
        current_region = result[4]
        current_city = result[5]
        add_city_to_region(result_pool,current_country,current_region,current_city)
        result_pool["port"].add(result[1])
        products = result[12].split(",")
        for product in products:
            result_pool["product"].add(product)

        # result_pool["country"][current_country][current_region].add(current_city)
    # print(result_pool)
    return result_pool


def check_search_key_exceed(search_key):
    '''size'''
    data = get_search_data(search_key)
    if data.get("size") > 10000:
        return True
    return False

def get_results(source_key,result_pool):
    link_results = set()

    client = Client(config.FOFA_KEY)
    data = client.search(source_key, size=10000, page=1,
                         fields="link")
    if data.get("size") > 10000:
        print(
            colorize("[-] 等待开发...", "red"))
        ## 城市
        country_result = []
        # for country_code, country_data in result_pool['country'].items():
        #
        #     for region_code, region_data in country_data.items():
        #         for city in region_data:
        #             country_result.append(
        #                 f'({source_key}) && country="{country_code}" && region="{region_code}" && city="{city}"')
        #
        # ## 产品
        # product_result = []
        # for search_key in country_result:
        #     for product in result_pool['product']:
        #         product_result.append(f'{search_key} && product="{product}"')
        #
        # ## 端口
        # port_result = []
        # for search_key in product_result:
        #     for port in result_pool["port"]:
        #         port_result.append(f'{search_key} && port="{port}"')

        # false_port_key = ""
        # for port in result_pool["port"]:
        #     false_port_key += f" && port != {port}"
        #
        # for search_key in country_result:
        #     port_result.append(f"{search_key} {false_port_key}")

        # return port_result
    else:
        print(
            colorize("[*] 未超过FOFA会员单次限制", "green"))
        link_results.update(data["results"])
        return link_results


# def get_results(search_key_result):
#     link_results = set()
#     for search_key in search_key_result:
#         links = get_link_results(search_key, 10000)
#         print(
#             colorize("[*] 当前搜索关键词: {}".format(search_key), "blue"))
#         link_results.update(links)
#     print(
#         colorize("[*] 搜索结束 去重后数量为: {}".format(len(link_results)), "blue"))
#     return link_results

import socket
from urllib.parse import urlparse


def is_ip(url):
    url = urlparse(url).netloc
    if ":" in url:
        url = url.split(":")[0]
    try:
        ip = socket.gethostbyname(url)
        if ip == url:
            return True
        else:
            return False
    except:
        return False

from tldextract import tldextract

def parse_url(url):
    parsed_url = urlparse(url)
    return parsed_url.scheme + "://" + parsed_url.netloc

def get_ip(url):
    parsed_url = urlparse(url)
    if ":" in parsed_url.netloc:
        return parsed_url.netloc.split(":")[0]
    return parsed_url.netloc

def save_scan_target(results):
    print(
        colorize("[*] 结果去重中...", "green"))
    result_set = set()
    with open('target.txt', 'w', encoding='utf-8') as file:
        for target in results:
            print(
                colorize("[*] 当前去重检测项: {}".format(target), "green"))
            if is_ip(target):
                ip = get_ip(target)
                if ip not in result_set:
                    # print('ip '+ip)
                    # print(parse_url(target))
                    file.write(target+"\n")
                    result_set.add(ip)
            else:
                url1 = tldextract.extract(target)
                host = url1.domain + "." + url1.suffix
                if host not in result_set:
                    # print('host '+host)
                    # print(parse_url(target))
                    file.write(target+"\n")
                    result_set.add(host)
        print(
            colorize("[*] 扫描结束,最终结果数量为 {}".format(len(result_set)), "blue"))

def get_result_from_api(source_key):
    result = get_base_results(source_key, 10000)
    # print(result)
    result_pool = init_result_pool(result)
    results = get_results(source_key, result_pool)
    save_scan_target(results)

if __name__ == "__main__":
    source_key_1='app="ASPCMS" && is_domain=true && country="CN" && region!="HK" && host!="gov.cn"'
    # source_key = '"tomcat" && icon_hash="-656811182"'
    get_result_from_api(source_key_1)
    # print(results)
    # print(result)
    # print(len(result))


