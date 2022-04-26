# -*- coding: utf-8 -*-

from qcloud_sdk.config import settings


class CosBaseAPIMixin(object):
    """
    通用API
    """
    def request_cos_bucket_api(self, method, path, query_params, headers, appid=None, region=None, bucket=None, stream=False):
        """
        对象存储存储桶通用API

        TODO：
          - 合并验证值的异常处理，一次抛出所有异常，以方便开发者一次排查一次修正。

        :param method:
        :param path:
        :param query_params:
        :param headers:
        :param appid:
        :param region:
        :param bucket:
        :param stream:
        :return:
        """
        appid = appid or settings.APPID
        if not appid:
            raise ValueError('APPID不可以为空')
        region = region or settings.COS_DEFAULT_REGION or settings.DEFAULT_REGION
        if not region:
            raise ValueError('地域不可以为空')
        bucket = bucket or settings.COS_DEFAULT_BUCKET
        if not bucket:
            raise ValueError('存储桶不可以为空')
        host = f'{bucket}-{appid}.cos.{region}.myqcloud.com'
        response = self.request_cos_api(method=method, host=host, path=path, query_params=query_params, headers=headers, stream=stream)
        # TODO: 分类处理文件和XML数据
        return response
