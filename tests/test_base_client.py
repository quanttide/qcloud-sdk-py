# -*- coding: utf-8 -*-

import unittest

from tests.client import APIClientTestCase


class BaseAPIClientTestCase(APIClientTestCase):
    def test_request_api(self):
        data = self.client.request_api(service='cvm', region='ap-shanghai', action='DescribeZones', params={},
                                       api_version='2017-03-12')
        self.assertTrue(data)


if __name__ == '__main__':
    unittest.main()