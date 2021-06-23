# -*- coding: utf-8 -*-
"""
云开发HTTP访问服务API，简化云开发HTTP访问服务的API请求方式。
"""

import requests


class CloudBaseHTTPClient(object):
    def __init__(self, env_id=None, qcloud_app_id=None, region=None, custom_domain=None):

        # 根域名
        if custom_domain:
            # 自定义域名
            self.domain = custom_domain
        else:
            # 云开发默认域名
            self.domain = env_id + '-' + qcloud_app_id + '.' + region + '.app.tcloudbase.com'

    def request(self, method, path, query_params=None, data=None):
        url = 'https://' + self.domain + path
        r = requests.request(method, url, params=query_params, data=data)
        # HTTP访问正常
        if r.status_code == requests.codes.ok:
            # JSON格式返回加工后数据
            if r.headers['content-type'] == 'application/json':
                return r.json()
            # 其他格式返回原始content
            else:
                return r.content
        # HTTP访问异常，即4XX或5XX
        else:
            # 抛出异常
            # 后续根据需要改进
            r.raise_for_status()

