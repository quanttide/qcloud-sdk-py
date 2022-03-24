# -*- coding: utf-8 -*-

import requests
import xmltodict

from qcloud_sdk.base.client import APIClientInitializer
from qcloud_sdk.cos.sign import calculate_auth_string


class CosBaseAPIClientMixin(object):
    def generate_cos_request_headers(self, host):
        """

        https://cloud.tencent.com/document/product/436/7728

        TODO:
          - 支持API传入头部
          - 支持服务端加密请求头部

        :param host:
        :return:
        """
        headers = {
            'Host': host,
            'Authorization': calculate_auth_string()
        }
        if self.session_token:
            headers['x-cos-security-token'] = self.session_token
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

    def request_cos_api(self, method, host):
        url = 'https://' + host
        r = requests.request(method, url)
        self.parse_cos_response_data(r.content)


class CosBaseAPIClient(APIClientInitializer, CosBaseAPIClientMixin):
    pass
