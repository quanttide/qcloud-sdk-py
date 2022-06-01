# -*- coding: utf-8 -*-

from qcloud_sdk.cos.api.base import CosBaseAPIMixin
from qcloud_sdk.cos.api.service import CosServiceAPIMixin
from qcloud_sdk.cos.api.bucket import CosBucketAPIMixin, CosBucketIntegratedAPIMixin
from qcloud_sdk.cos.api.object import CosObjectAPIMixin, CosObjectIntegratedAPIMixin


class CosAPIMixin(
    # 基本API
    CosBaseAPIMixin,
    # 对象存储服务API
    CosServiceAPIMixin,
    # 存储桶API
    CosBucketAPIMixin,
    CosBucketIntegratedAPIMixin,
    # 对象API
    CosObjectAPIMixin,
    CosObjectIntegratedAPIMixin
):
    """
    对象存储API
    """
    pass
