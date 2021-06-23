# -*- coding: utf-8 -*-

import unittest
import os

from qcloud_sdk.cloudbase.http import CloudBaseHTTPClient

# 环境变量
from environs import Env
Env().read_env()


class CloudBaseHTTPClientTestCase(unittest.TestCase):
    @classmethod
    def setUp(cls):
        cls.client = CloudBaseHTTPClient(
            env_id=os.environ.get('CLOUDBASE_ENV_ID'),
            qcloud_app_id=os.environ.get('TENCENT_APP_ID'),
            region=os.environ.get('TENCENT_REGION')
        )

    def test_request(self):
        """
        注意：云开发API可访问时测试可用。
        """
        data = self.client.request('POST', os.environ.get('CLOUDBASE_TEST_API_PATH'))
        self.assertTrue(data)


if __name__ == '__main__':
    unittest.main()
