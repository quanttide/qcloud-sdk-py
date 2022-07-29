"""
对象API测试
"""

import unittest
import os

from qcloud_sdk.config import settings
from qcloud_sdk.cos.utils import remove_if_exists

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
        response = self.client.head_object(object_key=self.object_key)
        self.assertTrue(response.content_length)

    def test_head_object_not_exists(self):
        """
        TODO
        :return:
        """
        response = self.client.head_object(object_key='fake-key')
        self.assertEqual(404, response.status_code)

    def test_get_object_with_range(self):
        content_length = 1024
        response = self.client.get_object(object_key=self.object_key, range_begin=0, range_end=content_length - 1)
        self.assertEqual(content_length, int(response.headers['Content-Length']))

    def test_post_object(self):
        pass

    def test_put_object(self):
        response = self.client.put_object(object_key='qcloud_sdk/fake-key', data='test')
        self.assertEqual(200, response.status_code)
        self.assertTrue(response.hash_crc64ecma > 0)

    def test_put_object_with_file(self):
        local_file_path = './test.txt'
        with open(local_file_path, 'wb') as f:
            f.write(b'test')
        response = self.client.put_object(object_key='qcloud_sdk/fake-key', data=open(local_file_path, 'rb'))
        self.assertEqual(200, response.status_code)
        os.remove(local_file_path)

    def test_put_object_with_no_content(self):
        response = self.client.put_object(object_key='qcloud_sdk/fake-key')
        self.assertEqual(200, response.status_code)
        self.assertEqual(0, response.hash_crc64ecma)

    def test_put_object_repeatedly(self):
        """
        重复上传会覆盖
        """
        response = self.client.put_object(object_key='qcloud_sdk/fake-key', data='test')
        self.assertEqual(200, response.status_code)
        response2 = self.client.put_object(object_key='qcloud_sdk/fake-key', data='test2')
        self.assertEqual(200, response2.status_code)

    def test_delete_object(self):
        """
        TODO: 通过mock代替真实请求
        """
        self.client.put_object(object_key='fake-key', data='test')
        response = self.client.delete_object(object_key='fake-key')
        self.assertEqual(204, response.status_code)

    def test_delete_object_not_exists(self):
        """
        Note：返回值和存在时没有区别。
        """
        self.assertFalse(self.client.exists_object('fake-object'))
        response = self.client.delete_object('fake-object')
        self.assertEqual(204, response.status_code)


class CosObjectIntegratedAPITestCase(APIClientTestCase):
    def setUp(self):
        # 云端对象Key
        self.object_key = settings.COS_TEST_OBJECT_KEY
        # 本地对象下载目标文件路径
        self.object_file_path = settings.COS_TEST_OBJECT_FILE_PATH
        # 本地对象下载原始文件路径
        self.object_raw_file_path = settings.COS_TEST_OBJECT_RAW_FILE_PATH

    def test_exists_object_true(self):
        object_exists = self.client.exists_object(self.object_key)
        self.assertTrue(object_exists)

    def test_exists_object_false(self):
        object_exists = self.client.exists_object('fake-key')
        self.assertFalse(object_exists)


class DownloadObjectTestCase(APIClientTestCase):
    """
    下载对象到本地文件API（downlaod_object_to_file）单元测试。
    """

    def setUp(self):
        # 云端对象Key
        self.object_key = settings.COS_TEST_OBJECT_KEY
        # 本地对象下载目标文件路径
        self.object_file_path = settings.COS_TEST_OBJECT_FILE_PATH
        # 本地对象下载临时文件路径
        self.object_tmp_file_path = settings.COS_TEST_OBJECT_FILE_PATH + '.tmp'
        # 本地对象下载原始文件路径
        self.object_raw_file_path = settings.COS_TEST_OBJECT_RAW_FILE_PATH

    def test_download_object_to_file(self):
        """
        大文件测试报告 (cos_object_example.txt)：
         - 云端文件大小：75.23MB
         - 本地下载大小：78.9MB
         - 本地原始文件大小：78.9MB
         - 运行时间：44s
        """
        self.client.download_object_to_file(object_key=self.object_key, file_path=self.object_file_path,
                                            remove_unverified_file=False)
        self.assertTrue(os.path.exists(self.object_file_path))

    def test_download_breakpoint_resume(self):
        """
        断点续传
        """
        # 模拟下载临时文件
        remove_if_exists(self.object_tmp_file_path)
        response = self.client.get_object(object_key=self.object_key, range_begin=0, range_end=1024 * 1024 - 1)
        response.save_object_to_file(self.object_tmp_file_path)
        self.assertTrue(os.path.exists(self.object_tmp_file_path))
        existed_size = os.path.getsize(self.object_tmp_file_path)
        # 断点续传
        result = self.client.download_object_to_file(object_key=self.object_key, file_path=self.object_file_path,
                                                     remove_unverified_file=False)
        # 验证文件是否下载
        self.assertTrue(os.path.exists(self.object_file_path))
        # 验证断点续传大小是否正确
        self.assertTrue(result['downloaded_size'] < result['file_size'])
        self.assertEqual(existed_size, result['file_size'] - result['downloaded_size'])

    def test_download_unverified_file(self):
        """
        下载无法通过验证的文件，验证是否删除。
        :return:
        """
        # 破坏中间临时文件，模拟验证异常
        with open(self.object_tmp_file_path, 'wb') as f:
            f.write(b'1234567890')
        with self.assertRaises(ValueError) as context:
            self.client.download_object_to_file(object_key=self.object_key, file_path=self.object_file_path,
                                                remove_unverified_file=True)
            self.assertIn('CRC64校验不通过', context.exception)
        self.assertFalse(os.path.exists(self.object_tmp_file_path))


if __name__ == '__main__':
    unittest.main()
