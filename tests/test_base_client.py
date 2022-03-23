# -*- coding: utf-8 -*-

import os
import unittest
from unittest import mock

from qcloud_sdk.base.client import APIClientInitializer, BaseAPIClient
from tests.utils import reload_settings


class APIClientInitializerTestCase(unittest.TestCase):
    def test_init_with_env(self):
        reload_settings()
        client = APIClientInitializer(secret_id='fake-secret-id', secret_key='fake-secret-key')
        self.assertEqual('fake-secret-id', client.secret_id)
        self.assertEqual('fake-secret-key', client.secret_key)
        self.assertFalse(client.session_token)

    def test_init_tmp_secrets_with_env(self):
        reload_settings()
        client = APIClientInitializer(secret_id='fake-tmp-secret-id', secret_key='fake-tmp-secret-key',
                                      session_token='fake-tmp-session-token')
        self.assertEqual('fake-tmp-secret-id', client.secret_id)
        self.assertEqual('fake-tmp-secret-key', client.secret_key)
        self.assertEqual('fake-tmp-session-token', client.session_token)


class BaseAPIClientTestCase(unittest.TestCase):
    def test_request_api(self):
        client = BaseAPIClient()
        data = client.request_api(service='cvm', region='ap-shanghai', action='DescribeZones', params={},
                                  api_version='2017-03-12')
        self.assertTrue(data)


if __name__ == '__main__':
    unittest.main()
