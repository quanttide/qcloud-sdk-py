# -*- coding: utf-8 -*-

import time

import requests

from .sign import cal_auth
from .exceptions import QCloudAPIException


class QCloudAPIClient(object):
    exception_class = QCloudAPIException

    def __init__(self, secret_id=None, secret_key=None, http_method='POST', content_type='application/json', sign_method='v3'):
        self.secret_id = secret_id
        self.secret_key = secret_key
        self.http_method = http_method
        assert content_type in ['application/json', 'application/x-www-form-urlencoded', 'multipart/form-data'], '错误的content-type'
        self.content_type = content_type
        assert sign_method in ['v3', 'TC3-HMAC-SHA256', 'v1', 'HmacSHA256', 'HmacSHA1'], '错误的签名方法'
        self.sign_method = sign_method

    def request_api(self, service: str, region: str, api: str, api_params: dict, **kwargs):
        """

        :param service: 云服务标签，比如`cvm`（云数据库）
        :param region: 地域
        :param api: 云API
        :param api_params: API参数
        :param kwargs:
        :return:
        """
        # 服务地址
        endpoint = '{service}.{region}.tencentcloudapi.com'.format(service=service, region=region)

        # 时间戳
        timestamp = int(time.time())

        # 公共参数
        if self.sign_method in ['v3', 'TC3-HMAC-SHA256']:
            # 签名方法 V3（也叫 TC3-HMAC-SHA256）
            headers = {
                'Content-Type': self.content_type,
                'X-TC-Action': api,
                'X-TC_Region': region,
                'X-TC-Timestamp': timestamp,
                'X-TC-Version': '2017-03-12',
                'Authorization': cal_auth(self.secret_id, self.secret_key, endpoint, service, api_params, timestamp),
            }
        elif self.sign_method in ['v1', 'HmacSHA256', 'HmacSHA1']:
            # 签名方法 V1（也叫 HmacSHA256 或 HmacSHA1）
            raise NotImplementedError('签名方法V1尚未实现')

        # 请求API
        url = "https://" + endpoint
        if self.http_method == 'POST':
            r = requests.post(url, headers=headers)
        elif self.http_method == 'GET':
            raise NotImplementedError('GET方法请求尚未实现')

        # 根据content-type解析数据
        if self.content_type == 'application/json':
            data = r.json()['Response']
        elif self.content_type == 'application/x-www-form-urlencoded':
            raise NotImplementedError('未实现此格式数据解析')
        elif self.content_type == 'multipart/form-data':
            raise NotImplementedError('未实现此格式数据解析')

        # 抛出API返回的异常
        if 'Error' in data:
            raise self.exception_class(request_id=data['RequestId'], err_code=data['Error']['Code'], err_msg=data['Error']['Message'])
        # 返回数据
        return data
