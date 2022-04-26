"""
对象API测试
"""

import unittest
import os

from qcloud_sdk.config import settings

from tests.client import APIClientTestCase


class CosObjectAPITestCase(APIClientTestCase):
    """
    对象API单元测试
    """
    def setUp(self):
        # 云端对象Key
        self.object_key = settings.COS_TEST_OBJECT_KEY
        # 本地对象下载目标文件路径
        self.object_file_path = settings.COS_TEST_OBJECT_FILE_PATH
        # 本地对象下载原始文件路径
        self.object_raw_file_path = settings.COS_TEST_OBJECT_RAW_FILE_PATH

    def test_head_object(self):
        self.client.head_object(object_key=self.object_key)

    def test_get_object_with_range(self):
        content_length = 1024
        response = self.client.get_object(object_key=self.object_key, range_begin=0, range_end=content_length-1)
        self.assertEqual(content_length, int(response.headers['content-length']))


class CosObjectCustomAPITestCase(APIClientTestCase):
    def setUp(self):
        # 云端对象Key
        self.object_key = settings.COS_TEST_OBJECT_KEY
        # 本地对象下载目标文件路径
        self.object_file_path = settings.COS_TEST_OBJECT_FILE_PATH
        # 本地对象下载原始文件路径
        self.object_raw_file_path = settings.COS_TEST_OBJECT_RAW_FILE_PATH

    def test_download_object_to_file(self):
        """
        测试报告：
         - 云端文件大小：75.23MB
         - 本地下载大小：78.9MB
         - 本地原始文件大小：78.9MB
         - 运行时间：44s
        """
        self.client.download_object_to_file(object_key=self.object_key, file_path=self.object_file_path,
                                            remove_unverified_file=False)
        self.assertTrue(os.path.exists(self.object_file_path))


if __name__ == '__main__':
    unittest.main()
