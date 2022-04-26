# -*- coding: utf-8 -*-

import requests

from qcloud_sdk.base.client import APIClientInitializer
from qcloud_sdk.cos.sign import calculate_auth_string
from qcloud_sdk.cos.models import CosAPIResponse


class CosBaseAPIClientMixin(object):
    def generate_cos_request_headers(self, method, host, path, query_params, headers):
        """

        https://cloud.tencent.com/document/product/436/7728

        TODO:
          - 支持POST等方法的必选参数
          - 支持API传入头部
          - 支持服务端加密请求头部

        :param method:
        :param host:
        :param path:
        :param query_params:
        :param headers:
        :param secret_id:
        :param secret_key:
        :return:
        """
        headers['Host'] = host
        headers['Content-Type'] = headers.get('Content-Type', 'application/xml')
        if self.session_token:
            headers['x-cos-security-token'] = self.session_token
        headers['Authorization'] = calculate_auth_string(method, path, query_params, headers, self.secret_id, self.secret_key)
        return headers

    def request_cos_api(self, method, host, path, query_params, headers, stream=False):
        url = 'https://' + host + path
        headers = self.generate_cos_request_headers(method, host, path, query_params, headers)
        r = requests.request(method=method, url=url, params=query_params, headers=headers, stream=stream)
        return CosAPIResponse(r, stream=stream)


class CosBaseAPIClient(APIClientInitializer, CosBaseAPIClientMixin):
    pass
