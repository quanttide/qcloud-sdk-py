"""
对象存储数据模型
"""
from typing import Optional

import requests
import xmltodict


class CosAPIRequest(object):
    pass


class CosAPIResponse(object):
    """
    对象存储响应数据

    Ref:
      - https://docs.python-requests.org/en/latest/api/#requests.Response
    """
    def __init__(self, raw_response: requests.Response, stream=False):
        # 原始请求对象
        self.raw_response = raw_response
        # feature flags
        self.stream = stream
        # 根据COS需求解析的属性
        self.status_code: int = raw_response.status_code
        self.headers: dict = dict(raw_response.headers)
        self.content_length: int = int(self.headers['Content-Length'])
        self.hash_crc64ecma: Optional[int] = int(self.headers['x-cos-hash-crc64ecma']) if 'x-cos-hash-crc64ecma' in self.headers else None
        self.data = None
        if stream:
            # 文件流
            self.raw_data = raw_response.raw
            # TODO: 使用S3Object作为data的值
        else:
            # XML原始数据
            self.raw_data = raw_response.content
            if self.raw_data:
                self.data = xmltodict.parse(self.raw_data)

    def to_dict(self):
        """
        转换为dict

        TODO: 增加对content-length等的二次处理

        :return: dict
        """
        return {
            'data': self.data,
            'raw_data': self.raw_data,
            'raw_response': self.raw_response,
            'stream': self.stream,
        }.update(dict(self.headers))

    def save_object_to_file(self, file_path, mode='wb', chunk_size=1024):
        """
        保存对象到本地文件。用于GET Object等API。

        :param file_path: 本地文件路径
        :param mode: 文件打开模式，默认为`wb`
        :param chunk_size: 每次写入文件的数据块大小，默认为1024字节
        :return:
        """
        # 验证raw
        if not self.stream:
            raise ValueError('非原始数据格式')
        # 保存到本地
        with open(file_path, mode) as fd:
            for chunk in self.raw_response.iter_content(chunk_size=chunk_size):
                fd.write(chunk)
