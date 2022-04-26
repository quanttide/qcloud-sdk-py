"""
对象存储API测试
"""

import unittest
import os

from qcloud_sdk.config import settings

from tests.client import APIClientTestCase


class CosAPITestCase(APIClientTestCase):
    def test_get_service(self):
        data = self.client.get_object_storage_service()
        self.assertTrue(data)


class BucketAPITestCase(APIClientTestCase):
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

    def test_list_all_objects(self):
        data = self.client.list_all_objects(prefix=self.prefix)
        # !注意：1个子目录+1500个文件
        self.assertEqual(1501, len(data))


class ObjectAPITestCase(APIClientTestCase):
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
        # 对象ETag
        self.object_etag = settings.COS_TEST_OBJECT_ETAG

    def test_head_object(self):
        self.client.head_object(object_key=self.object_key)

    def test_get_object_with_range(self):
        content_length = 1024
        response = self.client.get_object(object_key=self.object_key, range_begin=0, range_end=content_length-1)
        self.assertEqual(content_length, int(response.headers['content-length']))

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
