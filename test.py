# -*- coding: utf-8 -*-
from tookit.fofa_client import Client

def get_base_results(key,search_key,size=10000,page=1):
    client = Client(key)
    data = client.search(search_key, size=size, page=page,fields="link,port,protocol,country,region,city,as_number,as_organization,host,domain,os,"
                                "server,product")
    return data["results"]


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
    print(result_pool)
    return result_pool

def get_new_search_key_list(source_key,result_pool):
    search_key_result = []

    # 真

    ## 城市
    country_result = []
    for country_code, country_data in result_pool['country'].items():

        for region_code, region_data in country_data.items():
            for city in region_data:
                country_result.append(f'({source_key}) && country="{country_code}" && region="{region_code}" && city="{city}"')

    ## 产品
    product_result = []
    for search_key in country_result:
        for product in result_pool['product']:
            product_result.append(f'{search_key} && product="{product}"')


    ## 端口
    port_result = []
    for search_key in product_result:
        for port in result_pool["port"]:
            port_result.append(f'{search_key} && port="{port}"')


    # false_port_key = ""
    # for port in result_pool["port"]:
    #     false_port_key += f" && port != {port}"
    #
    # for search_key in country_result:
    #     port_result.append(f"{search_key} {false_port_key}")

    for result in port_result:
        print(result)


    return

if __name__ == "__main__":
    key = ''  # 输入key
    source_key = 'header="thinkphp" || header="think_template"'
    result = get_base_results(key,source_key,100)
    print(result)
    result_pool = init_result_pool(result)
    get_new_search_key_list(source_key,result_pool)
    # print(result)
    # print(len(result))


