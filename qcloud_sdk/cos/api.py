# -*- coding: utf-8 -*-


from qcloud_sdk.config import settings


class CosAPIMixin(object):
    """
    对象存储API
    """
    # ----- 通用API -----
    def request_bucket_api(self, method, appid=None, region=None, bucket=None):
        bucket = bucket or settings.COS_DEFAULT_BUCKET
        host = f'{bucket}-{appid}.cos.{region}.myqcloud.com'
        return self.request_cos_api(method=method, host=host)

    # ----- Service API -----
    def get_cos_service(self, region=None):
        if region:
            host = f'cos.{region}.myqcloud.com'
        else:
            host = 'service.cos.myqcloud.com'
        return self.request_cos_api(method='GET', host=host, path='/', query_params={}, headers={})['ListAllMyBucketsResult']

    # ----- 存储桶API -----
    def list_buckets(self, region=None):
        return self.get_cos_service(region=region)

    def get_bucket(self, region=None, bucket=None):
        """
        列出该存储桶内的部分或者全部对象。

        详见：https://cloud.tencent.com/document/product/436/7734

        :return:
        """
        return self.request_cos_api(method='GET', region=region, bucket=bucket)['ListBucketResult']

    # ----- 对象API -----
    def list_objects(self, **kwargs):
        """
        同`get_bucket`方法，列出该存储桶内的部分或者全部对象。

        详见：https://cloud.tencent.com/document/product/436/7734

        :return:
        """
        return self.get_bucket(**kwargs)

    def list_all_objects(self, **kwargs):
        """
        (high-level API) 获取存储桶下所有对象。

        基于`list_objects`封装。

        :param kwargs:
        :return:
        """
        is_truncated = True  # 被截断
        kwargs['Marker'] = kwargs.get('Marker', "")
        while is_truncated:
            data = self.list_objects(**kwargs)
            is_truncated = data['IsTruncated']
            if 'NextMarker' in data:
                marker = data['NextMarker']
            else:
                is_truncated = False
