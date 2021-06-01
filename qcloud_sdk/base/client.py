# -*- coding: utf-8 -*-

import os
import time

import requests

from .sign import join_auth
from .exception import QCloudAPIException


class QCloudAPIClient(object):
    exception_class = QCloudAPIException

    def __init__(self, secret_id=None, secret_key=None):
        """

        :param secret_id:
        :param secret_key:
        """
        self.secret_id = secret_id or os.environ.get('TENCENT_SECRET_ID')
        self.secret_key = secret_key or os.environ.get('TENCENT_SECRET_KEY')

    def request_api(self, service: str, api: str, api_params: dict, region=None, version='2017-03-12') -> dict:
        """

        :param service: 云服务标签，比如`cvm`（云数据库）
        :param api: 云API
        :param api_params: API参数
        :param region: 云服务可选地域
        :param version: API版本
        :return:
        """
        # 服务地址，默认就近接入
        endpoint = '{service}.tencentcloudapi.com'.format(service=service, region=region)

        # 时间戳
        timestamp = int(time.time())

        # 公共参数
        headers = {
            'Host': endpoint,
            'Content-Type': 'application/json',
            'X-TC-Action': api,
            'X-TC-Timestamp': str(timestamp),
            'X-TC-Version': version,
            'Authorization': join_auth(self.secret_id, self.secret_key, endpoint, service, api_params, timestamp),
        }
        if region:
            headers['X-TC-Region'] = region

        # 请求API
        url = "https://" + endpoint
        r = requests.post(url, headers=headers)

        # 解析数据
        data = r.json()['Response']

        # 抛出API返回的异常
        if 'Error' in data:
            raise self.exception_class(request_id=data['RequestId'], err_code=data['Error']['Code'], err_msg=data['Error']['Message'])
        # 返回数据
        return data
