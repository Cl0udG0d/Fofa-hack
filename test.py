
from fofa_hack import fofa
from tookit import fofaUseragent

import requests,sys,mmh3,codecs

def main():
    result_generator = fofa.api('protocol="socks5" && "Authentication"', endcount=1000)
    for data in result_generator:
        for proxy in data:
            proxies = {'http': "http://{}".format(proxy), "https": "https://{}".format(proxy)}
            print(fr'[-] test: ' + str(proxies))
            try:
                r = requests.get('https://www.taobao.com/help/getip.php', proxies=proxies, timeout=3)
                if 'ipCallback' in r.text:
                    print(fr'[*] success: ' + str(proxies))
            except requests.exceptions.ConnectionError:
                pass
            except requests.exceptions.ReadTimeout:
                pass
            except KeyboardInterrupt:
                print('用户退出')
                exit()
            except requests.exceptions.InvalidSchema:
                print('未检测到pysocks')
                print('pip install -U requests[socks]')
                print('pip install pysocks')
                exit()


def get_ip():
    proxies =  {'http': 'socks5://18.178.209.57:5555', 'https': 'socks5://18.178.209.57:5555'}
    response = requests.get('https://api64.ipify.org?format=json',proxies=proxies).json()
    return response["ip"]

def get_location():
    ip_address = get_ip()
    response = requests.get(f'https://ipapi.co/{ip_address}/json/').json()
    location_data = {
        "ip": ip_address,
        "city": response.get("city"),
        "region": response.get("region"),
        "country": response.get("country_name")
    }
    return location_data


if __name__ == '__main__':
    main()