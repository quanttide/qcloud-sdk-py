# -*- coding: utf-8 -*-

import json
import shutil

import urllib3

from qcloud_sdk.config import settings


class CosAPIMixin(object):
    """
    对象存储API
    """
    # ----- 通用API -----
    def request_bucket_api(self, method, path, query_params, headers, appid=None, region=None, bucket=None, stream=False):
        appid = appid or settings.APPID
        region = region or settings.COS_DEFAULT_REGION or settings.DEFAULT_REGION
        bucket = bucket or settings.COS_DEFAULT_BUCKET
        host = f'{bucket}-{appid}.cos.{region}.myqcloud.com'
        return self.request_cos_api(method=method, host=host, path=path, query_params=query_params, headers=headers, stream=stream)

    # ----- Service API -----
    def get_cos_service(self, region=None):
        if region:
            host = f'cos.{region}.myqcloud.com'
        else:
            host = 'service.cos.myqcloud.com'
        return self.request_cos_api(method='GET', host=host, path='/', query_params={}, headers={})['ListAllMyBucketsResult']

    # ----- 存储桶API -----
    def list_buckets(self, **kwargs):
        return self.get_cos_service(**kwargs)

    def get_bucket(self, region=None, bucket=None, prefix='', delimiter='',
                   marker='', max_keys=1000):
        """
        列出该存储桶内的部分或者全部对象。

        详见：https://cloud.tencent.com/document/product/436/7734

        备注：
          - 传入encoding-type=url时，NextMarker返回值无法直接使用。此处暂无必要，所以不传入此参数。

        :param region:
        :param bucket:
        :param prefix:
        :param delimiter:
        :param marker: 起始对象键标记，从该标记之后（不含）按照 UTF-8 字典序返回对象键条目
        :param max_keys:
        :return:
        """
        prefix = prefix or settings.COS_DEFAULT_PREFIX
        query_params = {'prefix': prefix, 'delimiter': delimiter,
                        'marker': marker, 'max-keys': max_keys}
        return self.request_bucket_api(method='GET', path='/', query_params=query_params,
                                       headers={}, region=region, bucket=bucket)['ListBucketResult']

    # ----- 对象API -----
    def list_objects(self, **kwargs):
        """
        同`get_bucket`方法，列出该存储桶内的部分或者全部对象。

        详见：https://cloud.tencent.com/document/product/436/7734

        :return:
        """
        return self.get_bucket(**kwargs)

    def list_all_objects(self, **kwargs) -> list:
        """
        (high-level API) 获取存储桶下所有对象。

        基于`list_objects`封装。

        :param kwargs:
        :return:
        """
        # 对象列表
        object_list = []
        # 是否被截断标记
        is_truncated = True
        # 起始对象键标记
        marker = kwargs.pop('marker', "")
        while is_truncated:
            # 请求API
            data = self.list_objects(marker=marker, **kwargs)
            # 加入返回值列表
            object_list.extend(data['Contents'])
            # 取结果中的截断值
            # 使用json模块解析字符串`'true'`为布尔值`True`
            is_truncated = json.loads(data['IsTruncated'])
            if 'NextMarker' in data:
                # 仅当响应条目有截断（IsTruncated 为 true）才会返回
                # 当需要继续请求后续条目时，将该节点的值作为下一次请求的marker参数传入
                marker = data['NextMarker']
        return object_list

    def get_object(self, object_key: str, bucket=None, region=None, appid=None) -> urllib3.response.HTTPResponse:
        """

        https://cloud.tencent.com/document/product/436/7753

        TODO:
          - 增加COS参数和requests参数。

        :param object_key: 对象Key
        :param file_path: 目标文件路径
        :param bucket:
        :param region:
        :param appid:
        :return: requests.Response.raw实例
        """
        # 处理参数
        # TODO: 增加API请求参数
        query_params = {}
        # TODO：增加API请求头
        headers = {}
        # 发请求
        return self.request_bucket_api('GET', path=f'/{object_key}', query_params=query_params, headers=headers,
                                       bucket=bucket, region=region, appid=appid, stream=True)

    def get_object_to_file(self, object_key, file_path, bucket=None, region=None, appid=None, chunk_size=1024):
        """

        Ref:
          - https://urllib3.readthedocs.io/en/latest/advanced-usage.html#streaming-and-i-o
          - https://stackoverflow.com/questions/13137817/how-to-download-image-using-requests/13137873#13137873

        :param object_key:
        :param file_path:
        :param bucket:
        :param region:
        :param appid:
        :param chunk_size:
        :return:
        """
        raw = self.get_object(object_key=object_key, bucket=bucket, region=region, appid=appid)
        with open(file_path, 'wb') as f:
            for chunk in raw.stream(chunk_size):
                f.write(chunk)
