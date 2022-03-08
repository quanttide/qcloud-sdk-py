# -*- coding: utf-8 -*-
"""
References:
    - https://cloud.tencent.com/document/product/436/12269
"""

from typing import List

from qcloud_cos import CosConfig, CosS3Client
from sts.sts import Sts

from django.conf import settings


# ----- COS API Client 设置 -----

COS_CONFIG = CosConfig(
    Region=settings.QCLOUD_PROJECT_REGION,
    SecretId=settings.QCLOUD_SECRET_ID,
    SecretKey=settings.QCLOUD_SECRET_KEY,
)
COS_BUCKET = settings.QCLOUD_COS_DEFAULT_FILE_BUCKET
COS_CLIENT = CosS3Client(COS_CONFIG)


# ----- 权限集设置 -----

# 只读
COS_PERMISSION_LIST_READONLY = [
    # 下载对象
    'name/cos:GetObject',
    # 查询对象元数据
    'name/cos:HeadObject',
]

# 读写
COS_PERMISSION_LIST_WRITE = [
    # 下载对象
    'name/cos:GetObject',
    # 查询对象元数据
    'name/cos:HeadObject',
    # 简单上传对象
    'name/cos:PutObject',
    # 分块上传
    "name/cos:InitiateMultipartUpload",
    "name/cos:ListMultipartUploads",
    "name/cos:ListParts",
    "name/cos:UploadPart",
    "name/cos:CompleteMultipartUpload",
    "name/cos:AbortMultipartUpload",
    # 表单上传对象
    "name/cos:PostObject",
    # 删除对象
    "name/cos:DeleteObject",
]


# ----- 临时密钥 -----

def is_allowed_actions(actions, allowed_strategy=None):
    permission_list_mapping = {
        'readonly': COS_PERMISSION_LIST_READONLY,
        'write': COS_PERMISSION_LIST_WRITE
    }
    if allowed_strategy is None:
        return True
    elif allowed_strategy in ['readonly', 'write']:
        return set(actions).issubset(set(permission_list_mapping[allowed_strategy]))
    else:
        raise Exception("传入错误的策略集选项")


def get_tmp_secret(allow_prefix: List[str], allow_actions: List[str], duration_seconds=None, allowed_strategy=None) -> dict:
    assert is_allowed_actions(allow_actions, allowed_strategy), '此策略集存在禁止的选项'

    if duration_seconds is None:
        duration_seconds = settings.QCLOUD_COS_TMP_SECRET_DURATION_SECONDS
    config = {
        'duration_seconds': duration_seconds,
        'secret_id': settings.QCLOUD_SECRET_ID,
        'secret_key': settings.QCLOUD_SECRET_KEY,
        'bucket': settings.QCLOUD_COS_BUCKET,
        'region': settings.QCLOUD_PROJECT_REGION,
        'allow_prefix': allow_prefix,
        # 密钥的权限列表
        # 权限列表请看 https://cloud.tencent.com/document/product/436/31923
        'allow_actions': allow_actions,
    }
    sts = Sts(config)
    response = sts.get_credential()
    return response


def get_tmp_secret_readonly(allow_prefix: List[str], duration_seconds=None) -> dict:
    allow_actions = [
        # 下载对象
        'name/cos:GetObject',
        # 查询对象元数据
        'name/cos:HeadObject',
    ]
    return get_tmp_secret(allow_prefix, allow_actions, duration_seconds)


def get_tmp_secret_write(allow_prefix: List[str], duration_seconds=None) -> dict:
    allow_actions = [
        # 下载对象
        'name/cos:GetObject',
        # 查询对象元数据
        'name/cos:HeadObject',
        # 简单上传对象
        'name/cos:PutObject',
        # 分块上传
        "name/cos:InitiateMultipartUpload",
        "name/cos:ListMultipartUploads",
        "name/cos:ListParts",
        "name/cos:UploadPart",
        "name/cos:CompleteMultipartUpload",
        "name/cos:AbortMultipartUpload",
        # 表单上传对象
        "name/cos:PostObject",
        # 删除对象
        "name/cos:DeleteObject",
    ]
    return get_tmp_secret(allow_prefix, allow_actions, duration_seconds)


# ----- 对象管理 -----

def upload_cos_object(fname):
    """
    对象上传接口，根据文件大小决定是否使用分块上传

    TODO
    :return:
    """
    response = COS_CLIENT.upload_file(Bucket=COS_BUCKET, Key=fname, LocalFilePath=fname)
    return response
