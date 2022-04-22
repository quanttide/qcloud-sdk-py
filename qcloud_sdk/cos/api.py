# -*- coding: utf-8 -*-

import os
import json

import urllib3
from tqdm import tqdm

from qcloud_sdk.config import settings
from qcloud_sdk.cos.utils import calculate_file_crc64


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

    # ----- 对象存储服务API -----
    def get_object_storage_service(self, region=None):
        if region:
            host = f'cos.{region}.myqcloud.com'
        else:
            host = 'service.cos.myqcloud.com'
        response = self.request_cos_api(method='GET', host=host, path='/', query_params={}, headers={})
        return response.data['ListAllMyBucketsResult']

    # ----- 存储桶API -----
    def list_buckets(self, **kwargs):
        return self.get_object_storage_service(**kwargs)

    def get_bucket(self, region=None, bucket=None, prefix='', delimiter='',
                   marker='', max_keys: int = 1000):
        """
        列出该存储桶内（或指定前缀）的对象和子目录。

        详见：https://cloud.tencent.com/document/product/436/7734

        备注：
          - 文件夹也会被单独列举，比如`qcloud_sdk`。
          - 传入encoding-type=url时，NextMarker返回值无法直接使用。此处暂无必要，所以不传入此参数。

        :param region:
        :param bucket:
        :param prefix: 前缀匹配。用来规定返回的文件前缀地址，也包括子目录。
        :param delimiter: 定界符为一个分隔符号，用于对对象键进行分组。一般是传`/`。
                          所有对象键从 Prefix 或从头（如未指定 Prefix）到首个 delimiter 之间相同部分的路径归为一类，
                          定义为 Common Prefix，然后列出所有 Common Prefix。
        :param marker: 起始对象键标记。从该标记之后（不含）按照 UTF-8 字典序返回对象键条目
        :param max_keys: 最大值。取值0-1000的整数，默认为1000。
        :return:
        """
        # 验证max_keys
        if not (isinstance(max_keys, int) and 0 <= max_keys <= 1000):
            raise ValueError('max_keys传参错误')
        # 前缀
        prefix = prefix or settings.COS_DEFAULT_PREFIX
        query_params = {'prefix': prefix, 'delimiter': delimiter,
                        'marker': marker, 'max-keys': max_keys}
        response = self.request_cos_bucket_api(method='GET', path='/', query_params=query_params,
                                               headers={}, region=region, bucket=bucket)
        return response.data['ListBucketResult']

    def list_objects(self, **kwargs):
        """
        同`get_bucket`方法。

        详见：https://cloud.tencent.com/document/product/436/7734

        :return:
        """
        return self.get_bucket(**kwargs)

    def list_all_objects(self, **kwargs) -> list:
        """
        (custom API) 获取存储桶下或指定目录下的所有子目录和对象。

        基于`list_objects`封装。

        备注：
          - 原始API无参数可以过滤子目录，因此需要开发者使用时特别注意过滤。

        TODO:
          - 以标准库`os.walk`的风格或其他合适的方式返回。

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

    # ----- 对象API -----
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
        # bugfix: 原本写成了`if range_begin and range_end`，当`range_begin=0`时会跳过条件。
        if (range_begin is not None) and (range_end is not None):
            headers['Range'] = f'bytes={range_begin}-{range_end}'
        # 发请求
        response = self.request_cos_bucket_api('GET', path=f'/{object_key}', query_params=query_params, headers=headers,
                                               bucket=bucket, region=region, appid=appid, stream=True)
        return response

    def download_object_to_file(self, object_key, file_path, bucket=None, region=None, appid=None,
                                request_chunk_size=1024*1024, file_chunk_size=1024,
                                remove_existed_file: bool = True,
                                remove_unverified_file: bool = True) -> None:
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
        :param file_chunk_size: 写入文件大小，默认为1k
        :param remove_existed_file: 是否删除下载前已存在文件，默认为True。
        :param remove_unverified_file: 是否删除结束下载以后未通过验证的文件，默认为True。
        :return:
        """
        # 清空下载前已存在文件
        if remove_existed_file and os.path.exists(file_path):
            os.remove(file_path)

        # 获取对象元数据
        headers = self.head_object(object_key=object_key, bucket=bucket, region=region, appid=appid)
        # 获取对象长度
        content_length = int(headers['content-length'])
        # 分块下载文件
        request_ranges = [(i, min(i-1+request_chunk_size, content_length)) for i in range(0, content_length, request_chunk_size)]
        for range_begin, range_end in tqdm(request_ranges):
            response = self.get_object(object_key=object_key, bucket=bucket, region=region, appid=appid,
                                       range_begin=range_begin, range_end=range_end)
            # 分块保存文件
            response.save_object_to_file(file_path, mode='ab', chunk_size=file_chunk_size)

        # CRC64校验
        # TODO：校验结果写入日志，包括CRC64的值、校验结果是否正确。
        if int(headers['x-cos-hash-crc64ecma']) != calculate_file_crc64(file_path, file_chunk_size):
            # 校验失败文件支持自动清空，以方便捕获异常后重新下载。
            if remove_unverified_file:
                os.remove(file_path)
            # TODO：换成自定义异常类，以方便被上级程序捕获。
            raise ValueError('CRC64校验不通过')
