import unittest

from qcloud_sdk.config import settings

from tests.client import APIClientTestCase


class EbAPITestCase(APIClientTestCase):
    def test_request_eb_api(self):
        data = self.client.request_eb_api(action='ListEventBuses', params={})
        self.assertTrue(data)

    def test_put_events(self):
        event_list = [
            # https://cloud.tencent.com/document/api/1359/67704#Event
            {
                'Source': '',
                'Data': 'application/json;charset=utf-8',
                'Type': 'COS:Created:PostObject',
                'Subject': f'qcs::dts:{settings.DEFAULT_REGION}:appid/uin:{settings.APPID}',
            }
        ]
        data = self.client.put_events(event_bus_id='default', event_list=event_list)
        self.assertTrue(data)
        print(data)


if __name__ == '__main__':
    unittest.main()
