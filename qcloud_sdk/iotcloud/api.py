"""

"""
import json

from qcloud_sdk.config import settings


class IoTCloudAPIMixin:
    def validate_iotcloud_api_params(self, params):
        if 'DeviceName' in params:
            # TODO：验证命名规则：[a-zA-Z0-9:_-]{1,60}
            pass
        return params

    def request_iotcloud_api(self, action, params, region=None, api_region=None):
        """

        :param action:
        :param params:
        :param region:
        :param api_region:
        :return:
        """
        params = self.validate_iotcloud_api_params(params)
        region = region or settings.IOTCLOUD_DEFAULT_REGION
        return self.request_api(service='iotcloud', action=action, params=params, region=region,
                                api_version='2021-04-08', api_region=api_region,
                                supported_regions=settings.IOTCLOUD_SUPPORTED_REGIONS,
                                supported_regions_doc=settings.IOTCLOUD_SUPPORTED_REGIONS_DOC)

    # ----- 产品API -----

    def describe_iot_products(self, offset: int, limit: int, **kwargs):
        """

        :param offset:
        :param limit:
        :param kwargs:
        :return:
        """
        if not (isinstance(offset, int) and offset >= 0):
            raise ValueError('偏移量从0开始取值的整数。')
        if not (isinstance(offset, int) and 10 <= limit <= 250):
            raise ValueError('分页大小取值范围为10-250的整数。')
        return self.request_iotcloud_api(action='DescribeProducts', params={'Offset': offset, "Limit": limit}, **kwargs)

    # ----- 设备API -----
    def update_iot_device_available_state(self, product_id: str, device_name: str, enable_state: int):
        if enable_state not in [0, 1]:
            raise ValueError("设备状态只可选0和1。")
        return self.request_iotcloud_api(action='UpdateDeviceAvailableState',
                                         params={'ProductId': product_id, 'DeviceName': device_name,
                                                 "EnableState": enable_state})

    # ----- 设备影子API  -----

    def describe_iot_device_shadow(self, product_id: str, device_name: str):
        """

        :param product_id:
        :param device_name: 命名规则：[a-zA-Z0-9:_-]{1,60}
        :return:
        """
        result = self.request_iotcloud_api(action='DescribeDeviceShadow',
                                           params={'ProductId': product_id, 'DeviceName': device_name})
        return json.loads(result['Data'])

    def update_iot_device_shadow(self, product_id: str, device_name: str, state: dict, shadow_version):
        result = self.request_iotcloud_api(action='UpdateDeviceShadow',
                                           params={'ProductId': product_id, 'DeviceName': device_name,
                                                   'State': json.dumps(state), 'ShadowVersion': shadow_version})
        return json.loads(result['Data'])
