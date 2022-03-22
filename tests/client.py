"""
测试APIClient实例
"""

import unittest

# 测试库
from qcloud_sdk.api import QCloudAPIClient


class APIClientTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # APIClient实例
        cls.client = QCloudAPIClient()
