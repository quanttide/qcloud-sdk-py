"""
对象存储请求签名测试

参考资料：
- 签名工具：https://cos5.cloud.tencent.com/static/cos-sign/
"""

import unittest

from qcloud_sdk.cos.sign import *
from qcloud_sdk.config import settings


class CosSignTestCase(unittest.TestCase):
    def setUp(self):
        self.method = 'GET'
        self.host = 'service.cos.myqcloud.com'
        self.path = '/'
        self.query_params = {}
        self.headers = {'Content-Type': 'application/xml', 'Host': self.host}
        self.begin_time = 1648134580
        self.expire = 3600
        self.key_time = '1648134580;1648138180'
        self.http_parameters = ''
        self.header_list = 'content-type;host'
        self.http_headers = 'content-type=application%2Fxml&host=service.cos.myqcloud.com'
        self.http_string = 'get\n/\n\ncontent-type=application%2Fxml&host=service.cos.myqcloud.com\n'
        self.string_to_sign = 'sha1\n1648134580;1648138180\n323944bc3a45e5f9c7273632f53013f844fe987c\n'

    def test_join_key_time(self):
        key_time = join_key_time(self.begin_time, self.expire)
        self.assertEqual(self.key_time, key_time)

    def test_calculate_sign_key(self):
        sign_key = calculate_sign_key(key_time=self.key_time, secret_key=settings.SECRET_KEY)
        self.assertEqual(settings.COS_TEST_SIGN_KEY, sign_key)

    def test_join_http_params(self):
        query_params = {
            'prefix': 'example-folder/',
            'delimiter': '/',
            'max-keys': 10,
        }
        encoded_keys, encoded_params = join_http_params(query_params)
        self.assertEqual('delimiter;max-keys;prefix', encoded_keys)
        self.assertEqual('delimiter=%2F&max-keys=10&prefix=example-folder%2F', encoded_params)

    def test_join_http_headers(self):
        header_list, http_headers = join_http_params(self.headers)
        self.assertEqual(self.header_list, header_list)
        self.assertEqual(self.http_headers, http_headers)

    def test_join_http_string(self):
        http_string = join_http_string(self.method, self.path, self.http_parameters, self.http_headers)
        self.assertEqual(self.http_string, http_string)

    def test_calculate_string_to_sign(self):
        string_to_sign = calculate_string_to_sign(self.key_time, self.http_string)
        self.assertEqual(self.string_to_sign, string_to_sign)

    def test_calculate_signature(self):
        signature = calculate_signature(settings.COS_TEST_SIGN_KEY, self.string_to_sign)
        self.assertEqual(settings.COS_TEST_SIGN, signature)

    def test_calculate_auth_string(self):
        auth_string = calculate_auth_string(method=self.method, path=self.path,
                                            query_params=self.query_params,
                                            headers=self.headers,
                                            secret_id=settings.SECRET_ID,
                                            secret_key=settings.SECRET_KEY,
                                            begin_time=1648134580, expire=3600)
        self.assertEqual(settings.COS_TEST_AUTH_STRING, auth_string)


if __name__ == '__main__':
    unittest.main()
