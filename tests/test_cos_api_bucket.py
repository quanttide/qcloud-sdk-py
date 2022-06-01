"""
存储桶API测试
"""

import unittest
import os

from qcloud_sdk.config import settings

from tests.client import APIClientTestCase


class CosBucketAPITestCase(APIClientTestCase):
    """
    存储桶API单元测试
    """
    def setUp(self):
        # 默认文件夹
        self.prefix = settings.COS_TEST_BUCEKT_PREFIX
        self.next_marker = settings.COS_TEST_BUCEKT_NEXT_MARKER

    def test_get_bucket(self):
        data = self.client.get_bucket()
        self.assertTrue(data)
        self.assertTrue('Contents' in data)

    def test_list_objects(self):
        data = self.client.list_objects(prefix=self.prefix)
        self.assertTrue(data)
        # 不携带delimiter参数时不返回CommonPrefixes
        self.assertFalse('CommonPrefixes' in data)

    def test_list_objects_with_mark(self):
        data = self.client.list_objects(prefix=self.prefix, marker=self.next_marker)
        self.assertTrue(data)

    def test_list_objects_with_delimiter(self):
        data = self.client.list_objects(prefix=self.prefix, delimiter='/')
        self.assertTrue(data)
        # 携带delimiter参数时返回CommonPrefixes
        self.assertTrue('CommonPrefixes' in data)
        print(data['CommonPrefixes'])


class CosBucketIntegratedAPITestCase(APIClientTestCase):
    def setUp(self):
        # 默认文件夹
        self.prefix = settings.COS_TEST_BUCEKT_PREFIX

    def test_list_all_objects(self):
        data = self.client.list_all_objects(prefix=self.prefix)
        # !注意：1个子目录+1500个文件
        self.assertEqual(1501, len(data))


if __name__ == '__main__':
    unittest.main()
