"""
CLS日志服务API
"""

import unittest

from tests.client import APIClientTestCase
from qcloud_sdk.config import settings


class ClsAPITestCase(APIClientTestCase):
    @unittest.skip('待完成')
    def test_search_log(self):
        self.client.search_log(topic_id=settings.CLS_TEST_TOPIC_ID, timestamp_from='', timestamp_to='', )


if __name__ == '__main__':
    unittest.main()
