#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: Erdog, Loveforkeeps, Alluka
import base64
import json
import logging
import requests
import os
import sys

from retry.api import retry_call

if __name__ == '__main__':
    # 当作为脚本直接执行时的处理方式
    from exception import FofaError
    from helper import get_language, encode_query
else:
    # 当作为包/模块导入时的处理方式
    from .exception import FofaError
    from .helper import get_language, encode_query

class Client:
    """
    A class representing the FOFA client.

    :param key: The Fofa api key. If not specified, it will be read from the FOFA_KEY environment variable.
    :type key: str
    :param base_url: The base URL of the FOFA API. Defaults to 'https://fofa.info'.
    :type base_url: str
    :param proxies:  A proxies array for the requests library, e.g. {'https': 'your proxy'}
    :type proxies: dict

    """

    def __init__(self, key='', base_url='', proxies=None):
        """ Initialize the FOFA client.
        """
        if key == '':
            key = os.environ.get('FOFA_KEY', '')

        if base_url == '':
            base_url = os.environ.get('FOFA_BASE_URL', 'https://fofa.info')

        self.key = key

        self.base_url = base_url.rstrip('/')

        self.lang = 'en'
        sys_lang = get_language()
        if sys_lang != None and sys_lang.startswith('zh'):
            self.lang = 'zh-CN'

        self._session = requests.Session()
        if proxies:
            self._session.proxies.update(proxies)
            self._session.trust_env = False

        # retry config, in seconds
        self.tries = 5       # Number of retry attempts
        self.delay = 1       # Initial delay between retries
        self.max_delay = 60  # Maximum delay between retries
        self.backoff = 2     # Backoff factor for exponential backoff

    def get_userinfo(self):
        """
        Get user info for current user.
    
        :return: User information in JSON format.
        :rtype: dict
        :raises FofaException: If an error occurs during the API request.
       
        :Example:
        
        The returned JSON result will be in the following format:
        
        .. code-block:: json
        
            {
                "username": "sample",
                "fofacli_ver": "4.0.3",
                "fcoin": 0,
                "error": false,
                "fofa_server": true,
                "avatar": "https://nosec.org/missing.jpg",
                "vip_level": 0,
                "is_verified": false,
                "message": "",
                "isvip": false,
                "email": "username@sample.net"
            }

         """
        return self.__do_req( "/api/v1/info/my")

    def search(self, query_str, page=1, size=100, fields="", opts={}):
        """
        Search data in FOFA.

        :param query_str: The search query string.

            Example 1:
                'ip=127.0.0.1'
    
            Example 2:
                'header="thinkphp" || header="think_template"'

        :type query_str: str
        :param page: Page number. Default is 1.
        :type page: int
        :param size: Number of results to be returned in one page. Default is 100.
        :type size: int
        :param fields: Comma-separated list of fields to be included in the query result.
            Example:
            'ip,city'
        :type fields: str
        :param opts: Additional options for the query. This should be a dictionary of key-value pairs.
        :type opts: dict
        :return: Query result in JSON format.
        :rtype: dict
        
        .. code-block:: json
        
            {
                "results": [
                    [
                        "111.**.241.**:8111",
                        "111.**.241.**",
                        "8111"
                    ],
                    [
                        "210.**.181.**",
                        "210.**.181.**",
                        "80"
                    ]
                ],
                "mode": "extended",
                "error": false,
                "query": "app=\\"网宿科技-公司产品\\"",
                "page": 1,
                "size": 2
            }

        """
        param = opts
        param['qbase64'] = encode_query(query_str)
        param['page'] = page
        param['fields'] = fields
        param['size'] = size
        logging.debug("search '%s' page:%d size:%d", query_str, page, size)
        return self.__do_req('/api/v1/search/all', param)

    def can_use_next(self):
        """
        Check if the "search_next" API can be used.

        :return: True if the "search_next" API can be used, False otherwise.
        :rtype: bool
        """
        try:
            self.search_next('bad=query', size=1)
        except FofaError as e:
            if e.code == 820000:
                return True
            return False

    def search_next(self, query_str, fields='', size=100, next='', full=False, opts={}):
        """
        Query the next page of search results.

        :param query_str: The search query string.

            Example 1:
                'ip=127.0.0.1'
    
            Example 2:
                'header="thinkphp" || header="think_template"'

        :param fields: The fields to be included in the response.
            Default: 'host,ip,port'
        :type fields: str

        :param size: The number of results to be returned per page.
            Default: 100
            Maximum: 10,000
        :type size: int

        :param next: The ID for pagination.
            The next value is returned in the response of previous search query.
            If not provided, the first page of results will be returned.
        :type next: str

        :param full: Specify if all data should be searched.
            Default: False (search within the past year)
            Set to True to search all data.
        :type full: bool

        :param opts: Additional options for the search.
        :type opts: dict

        :return: The query result in JSON format.
        :rtype: dict
        """
        param = opts
        param['qbase64'] = encode_query(query_str)
        param['fields'] = fields
        param['size'] = size
        param['full'] = full
        if next and next != '':
            param['next'] = next

        logging.debug("search next for '%s' size:%d, next:%s", query_str, size, next)
        return self.__do_req('/api/v1/search/next', param)

    def search_stats(self, query_str, size=5, fields='', opts={}):
        """
        Query the statistics of the search results.

        :param query_str: The search query string.

            Example 1:
                'ip=127.0.0.1'
    
            Example 2:
                'header="thinkphp" || header="think_template"'

        :type query_str: str

        :param size: The number of results to be aggregated for each item.
            Default: 5
        :type size: int

        :param fields: The fields to be included in the aggregation.
            Example: 'ip,city'
        :type fields: str

        :param opts: Additional options for the search.
        :type opts: dict

        :return: query result in json format


        .. code-block:: json

            {
                "distinct": {
                    "ip": 1717,
                    "title": 411
                },
                "lastupdatetime": "2022-06-17 13:00:00",
                "aggs": {
                    "title": [
                        {
                            "count": 35,
                            "name": "百度一下，你就知道"
                        },
                        {
                            "count": 25,
                            "name": "百度网盘-免费云盘丨文件共享软件丨超大容量丨存储安全"
                        },
                        {
                            "count": 16,
                            "name": "百度智能云-登录"
                        },
                        {
                            "count": 2,
                            "name": "百度翻译开放平台"
                        }
                    ],
                    "countries": []
                },
                "error": false
            }

        """
        param = opts
        param['qbase64'] = encode_query(query_str)
        param['fields'] = fields
        param['size'] = size
        return self.__do_req('/api/v1/search/stats', param)

    def search_host(self, host, detail=False, opts={}):
        """
        Search for host information based on the specified IP address or domain.

        :param host: The IP address or domain of the host to search for.
        :type host: str
        :param detail: Optional. Specifies whether to show detailed information. Default is False.
        :type detail: bool
        :param opts: Optional. Additional options for the search. Default is an empty dictionary.
        :type opts: dict
        :return: The query result in JSON format.
        :rtype: dict

        .. code-block:: json

           {
                "error": false,
                "host": "78.48.50.249",
                "ip": "78.48.50.249",
                "asn": 6805,
                "org": "Telefonica Germany",
                "country_name": "Germany",
                "country_code": "DE",
                "protocol": [
                    "http",
                    "https"
                ],
                "port": [
                    80,
                    443
                ],
                "category": [
                    "CMS"
                ],
                "product": [
                    "Synology-WebStation"
                ],
                "update_time": "2022-06-11 08:00:00"
            }

        """
        param = opts
        param['detail'] = detail

        u = '/api/v1/host/%s' % host
        return self.__do_req(u, param)

    def __do_req(self, path, params=None, method='get'):
        u = self.base_url + path
        data = None
        req_param = {}

        if not self.key or self.key == '':
            raise FofaError("Empty fofa api key")

        if params == None:
            req_param = {
                "key": self.key,
                "lang": self.lang,
            }
        else:
            req_param = params
            req_param['key'] = self.key
            req_param['lang'] = self.lang

        if method == 'post':
            data = params
            params = None

        def make_request():
            headers = {"Accept-Encoding": "gzip"}
            response = self._session.request(url=u, method=method, data=data, params=req_param, headers=headers)
            if response.status_code != 200:
                raise Exception("Request failed with status code: {}".format(response.status_code))
            return response
        res = retry_call(make_request,
                         tries = self.tries,
                         delay = self.delay,
                         max_delay = self.max_delay,
                         backoff=self.backoff)
        data = res.json()
        if 'error' in data and data['error']:
            raise FofaError(data['errmsg'])
        return data

if __name__ == "__main__":
    client = Client()
    logging.basicConfig(level=logging.DEBUG)
    print(client.can_use_next())
    print(json.dumps(client.get_userinfo(), ensure_ascii=False))
    print(json.dumps(client.search('app="网宿科技-公司产品"', page=1), ensure_ascii=False))
    print(json.dumps(client.search_host('78.48.50.249', detail=True), ensure_ascii=False))
    print(json.dumps(client.search_stats('domain="baidu.com"', fields='title'), ensure_ascii=False))
