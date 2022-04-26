# -*- coding: utf-8 -*-


class CosServiceAPIMixin(object):
    """
    对象存储服务API
    """
    def get_object_storage_service(self, region=None):
        if region:
            host = f'cos.{region}.myqcloud.com'
        else:
            host = 'service.cos.myqcloud.com'
        response = self.request_cos_api(method='GET', host=host, path='/', query_params={}, headers={})
        return response.data['ListAllMyBucketsResult']

    def list_buckets(self, **kwargs):
        return self.get_object_storage_service(**kwargs)
