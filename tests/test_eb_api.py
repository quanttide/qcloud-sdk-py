import unittest

from qcloud_sdk.models.events import QCloudEvent

from tests.client import APIClientTestCase
from tests.test_eb_models import TestDataMixin


class EbAPITestCase(APIClientTestCase, TestDataMixin):
    def setUp(self):
        TestDataMixin.setUp(self)
        self.event = QCloudEvent(**self.event_raw)

    def test_request_eb_api(self):
        data = self.client.request_eb_api(action='ListEventBuses', params={})
        self.assertTrue(data)

    # ----- 事件集 -----
    def test_list_event_buses(self):
        data = self.client.list_event_buses()
        self.assertTrue(data)
        # print(data)

    def test_put_events(self):
        event_list = [self.event.to_dict()]
        data = self.client.put_events(event_list=event_list)
        self.assertTrue(data)
        # print(data)

    # ----- 事件规则 -----
    @unittest.skip('TODO')
    def test_create_event_rules(self):
        pass

    # ----- 事件连接器 -----
    @unittest.skip('TODO')
    def test_create_event_connection(self):
        pass


if __name__ == '__main__':
    unittest.main()
