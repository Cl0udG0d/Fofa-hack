import requests
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

print(get_ip())
# print(get_location())