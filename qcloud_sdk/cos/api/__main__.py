# -*- coding: utf-8 -*-

from qcloud_sdk.cos.api.base import CosBaseAPIMixin
from qcloud_sdk.cos.api.service import CosServiceAPIMixin
from qcloud_sdk.cos.api.bucket import CosBucketAPIMixin, CosBucketCustomAPIMixin
from qcloud_sdk.cos.api.object import CosObjectAPIMixin, CosObjectCustomAPIMixin


class CosAPIMixin(
    # 基本API
    CosBaseAPIMixin,
    # 对象存储服务API
    CosServiceAPIMixin,
    # 存储桶API
    CosBucketAPIMixin,
    CosBucketCustomAPIMixin,
    # 对象API
    CosObjectAPIMixin,
    CosObjectCustomAPIMixin
):
    """
    对象存储API
    """
    pass
