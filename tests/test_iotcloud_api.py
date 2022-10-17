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
                                                      device_name=settings.IOTCLOUD_TEST_DEVICE_NAME,
                                                      mock=True)
        self.assertTrue('payload' in data)
        self.assertTrue('metadata' in data['payload'])
        self.assertTrue('version' in data['payload'])

    def test_update_iot_device_shadow(self):
        # https://iotcloud.mock.tencentcloudapi.com/?tag=default&action=UpdateDeviceShadow&version=2021-04-08
        expected_data = {
            'payload': {
                'state': {
                    'desired': {
                        'color': 'red'
                    }
                },
                'metadata': {
                    'desired': {
                        'color': {
                            'timestamp': 1509092895971
                        }
                    }
                },
                'timestamp': 1509443636326,
                'version': 5
            },
            'result': 0,
            'timestamp': 1509440846582,
            'type': 'update'
        }
        data = self.client.update_iot_device_shadow(product_id='fake-id',
                                                    device_name='fake-name',
                                                    state={'desired': {'color': 'red'}},
                                                    shadow_version=4,
                                                    mock=True)
        self.assertDictEqual(data, expected_data)


if __name__ == '__main__':
    unittest.main()
