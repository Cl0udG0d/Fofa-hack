import json

import requests

from tookit import config, fofaUseragent


request_url="https://api.fofa.info/v1/m/profile"
# au = config.AUTHORIZATION_LIST[0]
# print(au)


rep = requests.get(request_url, headers=fofaUseragent.getFofaPageNumHeaders(), timeout=10)
print(json.loads(rep.text)["data"]["info"]["data_limit"])


request_url2 = "https://api.fofa.info/v1/m/data_usage/month"
rep = requests.get(request_url2, headers=fofaUseragent.getFofaPageNumHeaders(), timeout=10)
print(json.loads(rep.text)["data"])

# au = config.AUTHORIZATION_LIST.pop()
# print(au)
# print(config.AUTHORIZATION_LIST)