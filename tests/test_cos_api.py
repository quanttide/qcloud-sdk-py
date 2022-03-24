"""
对象存储API测试
"""

import unittest

from tests.client import APIClientTestCase


class CosAPITestCase(APIClientTestCase):
    def test_get_service(self):
        data = self.client.get_cos_service()
        print(data)


if __name__ == '__main__':
    unittest.main()
