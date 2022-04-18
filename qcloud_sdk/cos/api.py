# -*- coding: utf-8 -*-

import os
import json

import urllib3

from qcloud_sdk.config import settings


class CosAPIMixin(object):
    """
    对象存储API
    """
    # ----- 通用API -----
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

    # ----- Service API -----
    def get_cos_service(self, region=None):
        if region:
            host = f'cos.{region}.myqcloud.com'
        else:
            host = 'service.cos.myqcloud.com'
        response = self.request_cos_api(method='GET', host=host, path='/', query_params={}, headers={})
        return response.data['ListAllMyBucketsResult']

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
        response = self.request_cos_bucket_api(method='GET', path='/', query_params=query_params,
                                               headers={}, region=region, bucket=bucket)
        return response.data['ListBucketResult']

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
        (custom API) 获取存储桶下所有对象。

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

    def head_object(self, object_key: str, bucket=None, region=None, appid=None):
        """

        :param object_key: 对象键
        :param bucket: 存储桶，默认为COS_DEFAULT_BUCKET
        :param region: 地域，默认为COS_DEFAULT_REGION
        :param appid: APPID，默认为APPID
        :return:
        """
        # TODO
        query_params = {}
        headers = {}
        response = self.request_cos_bucket_api(method='HEAD', path=f'/{object_key}', query_params=query_params, headers=headers,
                                               bucket=bucket, region=region, appid=appid)
        return response.headers

    def get_object(self, object_key: str, bucket=None, region=None, appid=None,
                   range_begin=None, range_end=None) -> urllib3.response.HTTPResponse:
        """

        https://cloud.tencent.com/document/product/436/7753

        TODO:
          - 增加COS参数和requests参数。

        :param object_key: 对象Key
        :param bucket:
        :param region:
        :param appid:
        :param range_begin: 开始字节，包含
        :param range_end: 结束字节，包含
        :return: requests.Response.raw实例
        """
        # 处理参数
        # TODO: 增加API请求参数
        query_params = {}
        # TODO：增加API请求头
        headers = {}
        if range_begin and range_end:
            headers['Range'] = f'bytes={range_begin}-{range_end}'
        # 发请求
        response = self.request_cos_bucket_api('GET', path=f'/{object_key}', query_params=query_params, headers=headers,
                                               bucket=bucket, region=region, appid=appid, stream=True)
        return response

    def download_object_to_local_file(self, object_key, file_path, bucket=None, region=None, appid=None,
                                      request_chunk_size=1024*1024, write_chunk_size=1024):
        """
        (custom API) 下载对象为本地文件

        Ref:
          - https://urllib3.readthedocs.io/en/latest/advanced-usage.html#streaming-and-i-o
          - https://stackoverflow.com/questions/13137817/how-to-download-image-using-requests/13137873#13137873

        :param object_key:
        :param file_path:
        :param bucket:
        :param region:
        :param appid:
        :param request_chunk_size: 网络请求大小，默认为1M
        :param write_chunk_size: 写入文件大小，默认为1k
        :return:
        """
        headers = self.head_object(object_key=object_key, bucket=bucket, region=region, appid=appid)
        content_length = int(headers['content-length'])
        request_ranges = [(i, min(i-1+request_chunk_size, content_length)) for i in range(0, content_length, request_chunk_size)]
        # 清空文件
        if os.path.exists(file_path):
            os.remove(file_path)
        # 分块下载文件
        for range_begin, range_end in request_ranges:
            response = self.get_object(object_key=object_key, bucket=bucket, region=region, appid=appid,
                                       range_begin=range_begin, range_end=range_end)
            # 分块保存文件
            response.save_object_to_local_file(file_path, mode='ab', chunk_size=write_chunk_size)
