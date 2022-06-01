# -*- coding: utf-8 -*-

import json

from qcloud_sdk.config import settings


class CosBucketAPIMixin(object):
    """
    存储桶API
    """
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


class CosBucketIntegratedAPIMixin(object):
    def list_all_objects(self, **kwargs) -> list:
        """
        (Integrated API) 获取存储桶下或指定目录下的所有子目录和对象。

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
