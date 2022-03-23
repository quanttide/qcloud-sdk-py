"""
APIClient基本类
"""

import time
from typing import List, Optional

import requests

from qcloud_sdk.base.sign import calculate_auth_string
from qcloud_sdk.exceptions import QCloudAPIException
from qcloud_sdk.config import settings


class APIClientInitializer(object):
    def __init__(self, secret_id=None, secret_key=None, session_token=None):
        """

        :param secret_id: 密钥ID，session_token非空时为临时密钥ID
        :param secret_key: 密钥Key，session_token非空时为临时密钥Key
        :param session_token: 临时密钥Session Token
        """
        self.secret_id = secret_id or settings.SECRET_ID
        self.secret_key = secret_key or settings.SECRET_KEY
        self.session_token = session_token or settings.SESSION_TOKEN
        assert self.secret_id, "SecretID不可为空，请在实例化时传入secret_id参数或配置QCLOUD_SECRET_ID"
        assert self.secret_key, "SecretKey不可为空，请在实例化时传入secret_key参数或配置QCLOUD_SECRET_KEY"


class BaseAPIClientMixin(object):
    def generate_request_headers(self, endpoint, service, action, params, api_version, region=None, timestamp=None):
        """
        https://cloud.tencent.com/document/product/213/15692

        :param endpoint:
        :param service:
        :param action:
        :param params:
        :param api_version:
        :param region:
        :param timestamp:
        :return:
        """
        # 时间戳
        timestamp = timestamp or int(time.time())
        # 请求头
        headers = {
            'Host': endpoint,
            'Content-Type': 'application/json',
            'X-TC-Action': action,
            'X-TC-Timestamp': str(timestamp),
            'X-TC-Version': api_version,
            'Authorization': calculate_auth_string(self.secret_id, self.secret_key, endpoint, service, params, timestamp),
        }
        if region:
            headers['X-TC-Region'] = region
        if self.session_token:
            headers['X-TC-Token'] = self.session_token
        return headers

    def parse_response_data(self, response):
        # 解析数据
        data = response.json()['Response']
        # 抛出API返回的异常
        if 'Error' in data:
            raise QCloudAPIException(request_id=data['RequestId'], err_code=data['Error']['Code'], err_msg=data['Error']['Message'])
        # 返回数据
        return data

    def request_api(self, service: str, action: str, params: dict, api_version: str,
                    region: Optional[str] = None, supported_regions: Optional[List[str]] = None, supported_regions_doc: Optional[str] = None,
                    api_region: Optional[str] = None,) -> dict:
        """
        :param service: 云服务标签，比如`cvm`（云数据库）
        :param action: 云API，如``。
        :param params: API参数
        :param api_version: API版本。通常以云产品为单位指定。
        :param region: 云服务地域
        :param supported_regions: 此云服务支持地域列表
        :param supported_regions_doc: 云服务支持地域列表的文档
        :param api_region: API接入地域
        :return:
        """
        # 服务地址，默认就近接入
        if api_region:
            endpoint = f'{service}.{api_region}.tencentcloudapi.com'
        else:
            endpoint = f'{service}.tencentcloudapi.com'
        # 验证服务地域
        # 如果支持地域没有及时更新，可以通过环境变量覆盖默认参数。
        if region and supported_regions and (region not in supported_regions):
            raise ValueError(f'{region}不在支持地域列表中，请查阅文档{supported_regions_doc}确认是否在支持地域中。')
        # 公共参数
        headers = self.generate_request_headers(endpoint, service, action, params, api_version, region=region)
        # 请求API
        url = "https://" + endpoint
        r = requests.post(url, json=params, headers=headers)
        return self.parse_response_data(r)


class BaseAPIClient(APIClientInitializer, BaseAPIClientMixin):
    pass
