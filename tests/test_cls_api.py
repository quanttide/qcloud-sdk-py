"""
CLS日志服务API
"""

import unittest

from tests.client import APIClientTestCase
from qcloud_sdk.config import settings


class ClsAPITestCase(APIClientTestCase):
    def setUp(self):
        self.region = settings.TEST_CLS_REGION
        self.topic_id = settings.TEST_CLS_TOPIC_ID
        self.timestamp_from = settings.TEST_CLS_TIMESTAMP_FROM
        self.timestamp_to = settings.TEST_CLS_TIMESTAMP_TO

    def test_search_log(self):
        data = self.client.search_log(region=self.region, topic_id=self.topic_id,
                                      timestamp_from=self.timestamp_from, timestamp_to=self.timestamp_to,
                                      query='SCF_Type:*')
        self.assertTrue(data)


if __name__ == '__main__':
    unittest.main()
