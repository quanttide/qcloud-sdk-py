import unittest

from qcloud_sdk.config import settings

from tests.client import APIClientTestCase


class CosBaseAPITestCase(APIClientTestCase):
    def test_request_iotcloud_api(self):
        data = self.client.request_iotcloud_api(action='DescribeProducts', params={'Offset': 0, 'Limit': 10})
        self.assertTrue('Products' in data)
        self.assertTrue('TotalCount' in data)

    def test_describe_iot_products(self):
        data = self.client.describe_iot_products(offset=0, limit=10)
        self.assertTrue('Products' in data)
        self.assertTrue('TotalCount' in data)

    def test_update_iot_device_available_state(self):
        data = self.client.update_iot_device_available_state(product_id=settings.IOTCLOUD_TEST_PRODUCT_ID,
                                                             device_name=settings.IOTCLOUD_TEST_DEVICE_NAME,
                                                             enable_state=1)

    def test_describe_iot_device_shadow(self):
        data = self.client.describe_iot_device_shadow(product_id=settings.IOTCLOUD_TEST_PRODUCT_ID,
                                                      device_name=settings.IOTCLOUD_TEST_DEVICE_NAME)
        from pprint import pprint
        print('\n')
        pprint(data)
        self.assertTrue('payload' in data)
        self.assertTrue('metadata' in data['payload'])
        self.assertTrue('version' in data['payload'])

    def test_update_iot_device_shadow(self):
        shadow_version = self.client.describe_iot_device_shadow(product_id=settings.IOTCLOUD_TEST_PRODUCT_ID,
                                                                device_name=settings.IOTCLOUD_TEST_DEVICE_NAME)['payload']['version']
        data = self.client.update_iot_device_shadow(product_id=settings.IOTCLOUD_TEST_PRODUCT_ID,
                                                    device_name=settings.IOTCLOUD_TEST_DEVICE_NAME,
                                                    state={'desired': {'color': 'red'}}, shadow_version=shadow_version)
        self.assertEqual('red', data['payload']['state']['desired']['color'])


if __name__ == '__main__':
    unittest.main()
