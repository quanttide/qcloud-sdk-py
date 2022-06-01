"""
对象API
"""

import os
from typing import Dict, Union, Any

import urllib3
from tqdm import tqdm

from qcloud_sdk.cos.utils import verify_file_crc64, remove_if_exists, get_file_size


class CosObjectAPIMixin(object):
    """
    对象API
    """
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
        return dict(response.headers)

    def get_object(self, object_key: str, bucket=None, region=None, appid=None,
                   range_begin=None, range_end=None):
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


class CosObjectIntegratedAPIMixin(object):
    def download_object_to_file(self, object_key, file_path, bucket=None, region=None, appid=None,
                                request_chunk_size=1024*1024*20, file_chunk_size=1024*1024,
                                remove_existed_tmp_file: bool = False,
                                remove_unverified_file: bool = True,
                                raise_verification_error: bool = True) -> Dict[str, Union[int, Any]]:
        """
        (Integrated API) 下载对象为本地文件

        Ref:
          - https://urllib3.readthedocs.io/en/latest/advanced-usage.html#streaming-and-i-o
          - https://stackoverflow.com/questions/13137817/how-to-download-image-using-requests/13137873#13137873


        :param object_key:
        :param file_path:
        :param bucket:
        :param region:
        :param appid:
        :param request_chunk_size: 网络请求大小，默认为20M
        :param file_chunk_size: 写入文件大小，默认为1M
        :param remove_existed_tmp_file: 特性开关，是否删除下载前已存在的临时文件，默认为False，即为断点续传。
        :param remove_unverified_file: 特性开关，是否删除结束下载以后未通过验证的文件，默认为True。
        :param raise_verification_error: 特性开关，抛出验证异常，默认为True。
        :return:
        """
        # 临时文件路径
        tmp_file_path = file_path + '.tmp'
        # 特性开关打开时，清空临时文件，不断点续传
        remove_if_exists(tmp_file_path) if remove_existed_tmp_file else None
        # 计算已有临时文件大小
        existed_tmp_file_size = get_file_size(tmp_file_path)

        # 获取对象元数据
        headers = self.head_object(object_key=object_key, bucket=bucket, region=region, appid=appid)
        # 获取对象长度
        content_length = int(headers['Content-Length'])

        # 分块下载文件
        request_ranges = [(i, min(i-1+request_chunk_size, content_length)) for i in range(existed_tmp_file_size, content_length, request_chunk_size)]
        for range_begin, range_end in tqdm(request_ranges):
            response = self.get_object(object_key=object_key, bucket=bucket, region=region, appid=appid,
                                       range_begin=range_begin, range_end=range_end)
            # 分块保存文件
            response.save_object_to_file(tmp_file_path, mode='ab', chunk_size=file_chunk_size)

        # CRC64校验
        # TODO：校验结果写入日志，包括CRC64的值、校验结果是否正确。
        if not verify_file_crc64(int(headers['x-cos-hash-crc64ecma']), tmp_file_path, file_chunk_size):
            # 校验失败文件支持自动清空，以方便捕获异常后重新下载。
            os.remove(tmp_file_path) if remove_unverified_file else None
            # TODO：换成自定义异常类，以方便被上级程序捕获。
            raise ValueError('CRC64校验不通过') if raise_verification_error else None

        # 临时文件转正式文件
        os.rename(tmp_file_path, file_path)
        return {
            'file_size': content_length,
            'downloaded_size': content_length - existed_tmp_file_size,
        }
