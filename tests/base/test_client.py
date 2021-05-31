# -*- coding: utf-8 -*-

import unittest

from qcloud_sdk.base.client import *


# 导入环境变量
from environs import Env
env = Env()
env.read_env()


class QCloudAPIClientTestCase(unittest.TestCase):
    def test_request_api(self):
        client = QCloudAPIClient()
        client.request_api(service='cvm', region='ap-shanghai', api='DescribeZones', api_params={})


if __name__ == '__main__':
    unittest.main()