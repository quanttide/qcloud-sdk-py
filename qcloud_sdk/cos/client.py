# -*- coding: utf-8 -*-

import requests
import xmltodict

from qcloud_sdk.base.client import APIClientInitializer
from qcloud_sdk.cos.sign import calculate_auth_string


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

    def parse_cos_response_headers(self):
        """
        解析响应头部

        https://cloud.tencent.com/document/product/436/7729

        :return:
        """
        pass

    def parse_cos_response_data(self, raw_xml):
        return xmltodict.parse(raw_xml)

    def request_cos_api(self, method, host, path, query_params, headers, stream=False):
        url = 'https://' + host + path
        headers = self.generate_cos_request_headers(method, host, path, query_params, headers)
        r = requests.request(method=method, url=url, params=query_params, headers=headers, stream=stream)
        # 原始文件流
        # TODO: 增加POST等方法对stream的支持。
        if stream:
            return r.raw
        # 解析后的COS定义的XML格式数据
        return self.parse_cos_response_data(r.content)


class CosBaseAPIClient(APIClientInitializer, CosBaseAPIClientMixin):
    pass
