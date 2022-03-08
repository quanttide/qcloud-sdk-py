"""
腾讯云API
"""

from qcloud_sdk.base.client import APIClientInitializer, BaseAPIClientMixin
from qcloud_sdk.cos.client import CosBaseAPIClientMixin
from qcloud_sdk.cos.api import CosAPIMixin


class APIClient(
    APIClientInitializer,
    BaseAPIClientMixin,
    # 使用默认协议的云产品，使用BaseAPIClientMixin类。
    # 独立定义协议的云产品，使用其独立的APIClientMixin类。
    CosBaseAPIClientMixin,
    CosAPIMixin
):
    pass
