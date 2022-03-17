# -*- coding: utf-8 -*-

import unittest

from qcloud_sdk.base.sign import *


class SignatureTestCase(unittest.TestCase):
    # 模拟参数
    secret_id = 'gwegwegw'
    secret_key = 'gaeswaegew'
    region = 'ap-shanghai'
    service = 'cvm'
    endpoint = '{service}.tencentcloudapi.com'.format(service=service)
    api_params = {}
    timestamp = 1622478466
    date = '2021-05-31'

    # 官方工具生成的模拟签名结果
    official_canonical_request = 'POST\n/\n\ncontent-type:application/json\nhost:cvm.tencentcloudapi.com\n\ncontent-type;host\n44136fa355b3678a1146ad16f7e8649e94fb4fc21fe77e8310c060f61caaff8a'
    official_unsigned_string = 'TC3-HMAC-SHA256\n1622478466\n2021-05-31/cvm/tc3_request\nb7511c2a57e10458e52fe57af7b28c25796fc538db71eef3b256d94528d8834d'
    official_sign = 'dd0d3a39b291945b662ce15cc6370ce544cff20eda88693eec2cef1d7b76654a'
    official_auth = 'TC3-HMAC-SHA256 Credential=gwegwegw/2021-05-31/cvm/tc3_request, SignedHeaders=content-type;host, Signature=dd0d3a39b291945b662ce15cc6370ce544cff20eda88693eec2cef1d7b76654a'

    def test_join_canonical_request(self):
        canonical_request = join_canonical_request(self.endpoint, self.api_params)
        self.assertEqual(canonical_request, self.official_canonical_request)

    def test_join_unsigned_string(self):
        credential_scope = gen_canonical_scope(self.date, self.service)
        unsigned_string = join_unsigned_string(self.timestamp, credential_scope, self.official_canonical_request)
        self.assertEqual(unsigned_string, self.official_unsigned_string)

    def test_sign(self):
        signature = sign(self.secret_key, self.service, self.official_unsigned_string, self.date)
        self.assertEqual(signature, self.official_sign)

    def test_join_auth(self):
        auth = calculate_auth_string(secret_id=self.secret_id, secret_key=self.secret_key,
                                     endpoint=self.endpoint, service=self.service,
                                     api_params=self.api_params, timestamp=self.timestamp)
        self.assertEqual(auth, self.official_auth)


if __name__ == '__main__':
    unittest.main()
