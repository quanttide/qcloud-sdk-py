"""
对象存储
"""

import hashlib


# ----- S3对象 -----

class S3ObjectMetadata(object):
    """
    ETAG: range 不影响。
    CRC64: range get请求返回的将会是整个Object的crc64值。
    """
    pass


class S3Object(object):
    """
    S3对象模型

    假设从云API获取对象信息，和本地文件建立映射以方便上传下载API实现。

    关于S3对象：
      - Amazon S3 is an object store that uses unique key-values to store as many objects as you want.

    Ref:
      - https://docs.aws.amazon.com/AmazonS3/latest/userguide/UsingObjects.html
    """
    def __init__(self, key, version_id=None, value=None, metadata=None, sub_resources=None, acl=None):
        # 云端
        self.key = key
        self.version_id = version_id
        self.value = value
        self.metadata = metadata
        self.sub_resources = sub_resources
        self.acl = acl
