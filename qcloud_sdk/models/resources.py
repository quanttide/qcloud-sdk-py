"""
云资源数据模型
"""


class QCloudResource(object):
    """
    腾讯云资源

    Defined by CAM: https://cloud.tencent.com/document/product/598/10606
    """
    def __init__(self, service_type, region, account, resource):
        self.service_type = service_type
        self.region = region
        self.account = account
        self.resource = resource

    def to_string(self):
        return f'qcs::{self.service_type}:{self.region}:{self.account}:{self.resource}'

    def __str__(self):
        return self.to_string()

    def __repr__(self):
        return self.to_string()
