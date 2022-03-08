# -*- coding: utf-8 -*-
# 测试框架
import unittest

# 测试目标
from depreciated.ciam.api import CIAMAPIClient

# 环境变量
import os
from environs import Env
Env().read_env()


class CIAMAPIClientTestCase(unittest.TestCase):
    def setUp(self):
        self.client = CIAMAPIClient(
            client_id=os.environ['CIAM_CLIENT_ID'],
            client_secret=os.environ['CIAM_CLIENT_SECRET'],
            custom_portal_name=os.environ['CIAM_CUSTOM_PORTAL_NAME'],
        )

    def test_get_oidc_jwks(self):
        oidc_jwks = self.client.get_oidc_jwks()
        self.assertTrue('keys' in oidc_jwks)


if __name__ == '__main__':
    unittest.main()
