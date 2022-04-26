"""
对象存储API测试
"""

import unittest
import os

from qcloud_sdk.config import settings

from tests.client import APIClientTestCase


class CosServiceAPITestCase(APIClientTestCase):
    def test_get_service(self):
        data = self.client.get_object_storage_service()
        self.assertTrue(data)


if __name__ == '__main__':
    unittest.main()
