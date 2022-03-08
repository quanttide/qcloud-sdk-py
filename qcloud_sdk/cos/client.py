# -*- coding: utf-8 -*-

from qcloud_sdk.base.client import APIClientInitializer
from qcloud_sdk.cos.api import CosAPIMixin


class CosBaseAPIClientMixin(object):
    def generate_cos_request_headers(self):
        pass

    def parse_cos_response_data(self):
        pass

    def request_cos_api(self):
        pass


class CosBaseAPIClient(APIClientInitializer, CosBaseAPIClientMixin):
    pass


class CosAPIClient(CosBaseAPIClient, CosAPIMixin):
    pass
