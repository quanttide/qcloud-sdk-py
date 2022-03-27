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

    @unittest.skipUnless(settings.TEST_ALL, '避免消耗对象存储流量')
    def test_get_object_to_file(self):
        """
        测试报告：
         - 测试数据云端大小：304.66MB
         - 测试数据本地大小：319.5MB
         - 测试运行时间：27.891s
        """
        self.client.get_object_to_file(settings.COS_TEST_OBJECT_KEY, settings.COS_TEST_OBJECT_FILE_PATH)


if __name__ == '__main__':
    unittest.main()
