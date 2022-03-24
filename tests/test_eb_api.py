import unittest

from qcloud_sdk.scf.models import QCloudScfEvent

from tests.client import APIClientTestCase
from tests.test_models_events import TestDataMixin


class EbAPITestCase(APIClientTestCase, TestDataMixin):
    def setUp(self):
        TestDataMixin.setUp(self)
        self.event = QCloudScfEvent(**self.event_raw)

    def test_request_eb_api(self):
        data = self.client.request_eb_api(action='ListEventBuses', params={})
        self.assertTrue(data)

    # ----- 事件集 -----
    def test_list_event_buses(self):
        data = self.client.list_event_buses()
        self.assertTrue(data)
        # print(data)

    def test_put_events(self):
        event_list = [self.event]
        data = self.client.put_events(event_list=event_list)
        self.assertTrue(data)

    def test_put_event(self):
        data = self.client.put_event(event=self.event)
        self.assertTrue(data)

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
