"""
对象存储API测试
"""

import unittest

from qcloud_sdk.config import settings

from tests.client import APIClientTestCase


class CosAPITestCase(APIClientTestCase):
    def test_get_service(self):
        data = self.client.get_cos_service()
        self.assertTrue(data)

    def test_get_bucket(self):
        data = self.client.get_bucket()
        self.assertTrue(data)
        self.assertTrue('Contents' in data)

    def test_list_objects_with_mark(self):
        data = self.client.list_objects(marker=settings.COS_TEST_MARKER_OBJECT)
        self.assertTrue(data)

    def test_list_all_objects(self):
        data = self.client.list_all_objects()
        self.assertTrue(len(data) > 1000)


if __name__ == '__main__':
    unittest.main()
