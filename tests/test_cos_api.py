"""
对象存储API测试
"""

import unittest
import os

from qcloud_sdk.config import settings

from tests.client import APIClientTestCase


class CosAPITestCase(APIClientTestCase):
    def setUp(self):
        # 云端对象Key
        self.object_key = settings.COS_TEST_OBJECT_KEY
        # 本地对象下载目标文件路径
        self.object_file_path = settings.COS_TEST_OBJECT_FILE_PATH
        # 本地对象下载原始文件路径
        self.object_raw_file_path = settings.COS_TEST_OBJECT_RAW_FILE_PATH
        # 对象ETag
        self.object_etag = settings.COS_TEST_OBJECT_ETAG

    def test_get_service(self):
        data = self.client.get_cos_service()
        self.assertTrue(data)

    def test_get_bucket(self):
        data = self.client.get_bucket()
        self.assertTrue(data)
        self.assertTrue('Contents' in data)

    @unittest.skip('测试数据待重配')
    def test_list_objects_with_mark(self):
        data = self.client.list_objects(marker=settings.COS_TEST_MARKER_OBJECT)
        self.assertTrue(data)

    @unittest.skip('测试数据待重配')
    def test_list_all_objects(self):
        data = self.client.list_all_objects()
        self.assertTrue(len(data) > 1000)

    def test_head_object(self):
        self.client.head_object(object_key=self.object_key)

    def test_get_object_with_range(self):
        content_length = 1024
        response = self.client.get_object(object_key=self.object_key, range_begin=0, range_end=content_length-1)
        self.assertTrue(content_length, response.headers['content-length'])

    def test_download_object_to_local_file(self):
        """
        测试报告：
         - 云端文件大小：1.59M
         - 本地下载大小：2.3M
         - 本地原始文件大小：1.7M
         - 运行时间：1.415s
        """
        self.client.download_object_to_local_file(object_key=self.object_key, file_path=self.object_file_path)
        self.assertTrue(os.path.exists(self.object_file_path))


if __name__ == '__main__':
    unittest.main()
