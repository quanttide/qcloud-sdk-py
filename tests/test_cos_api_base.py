"""
对象存储API测试
"""

import unittest
import os

from qcloud_sdk.config import settings

from tests.client import APIClientTestCase


class CosBaseAPITestCase(APIClientTestCase):
    def test_request_cos_bucket_api(self):
        data = self.client.request_cos_bucket_api(method="GET", path='/', query_params={}, headers={})
        self.assertTrue(data)


if __name__ == '__main__':
    unittest.main()
