"""
对象API
"""

import os

import urllib3
from tqdm import tqdm
from qcloud_sdk.cos.utils import calculate_file_crc64


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


class CosObjectCustomAPIMixin(object):
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

