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
        self.path = '/'
        self.begin_time = 1648134580
        self.expire = 3600
        self.key_time = '1648134580;1648138180'
        self.http_parameters = 'max-keys=20'
        self.http_headers = 'content-type=image%2Fjpeg'
        self.http_string = 'get\n/\nmax-keys=20\ncontent-type=image%2Fjpeg\n'
        self.string_to_sign = 'sha1\n1648134580;1648138180\n368ec83b0b6a6963d664e8f7766c23e745558440\n'

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
        auth_string = calculate_auth_string(method='GET', path='/', query_params={'max-keys': 20},
                                            headers={'content-type': 'image/jpeg'},
                                            secret_id=settings.SECRET_ID,
                                            secret_key=settings.SECRET_KEY,
                                            begin_time=1648134580, expire=3600)
        self.assertEqual(settings.COS_TEST_AUTH_STRING, auth_string)


if __name__ == '__main__':
    unittest.main()
