"""
对象存储数据模型
"""

import hashlib

from requests import Response
import xmltodict


class CosRequestParams(object):
    pass


class CosResponseData(object):
    """
    对象存储响应数据

    Ref:
      - https://docs.python-requests.org/en/latest/api/#requests.Response
    """
    def __init__(self, response: Response, stream=False):
        self.response = response
        self.headers = response.headers
        self.stream = stream
        self.data = None
        if stream:
            # 文件流
            self.raw_data = response.raw
        else:
            # XML原始数据
            self.raw_data = response.content
            if self.raw_data:
                self.data = xmltodict.parse(self.raw_data)

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
            for chunk in self.response.iter_content(chunk_size=chunk_size):
                fd.write(chunk)
