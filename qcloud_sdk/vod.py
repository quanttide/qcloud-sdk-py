# -*- coding: utf-8 -*-
"""
腾讯云VOD云点播SDK

SDK组成：
- Python SDK：API接口封装；签名计算工具函数
- 超级播放器SDK：

安全机制：
- Referer防盗链：
- Key防盗链：超级播放器可以播放设置Key防盗链的视频，也可以通过构造Key防盗链URL直接访问未加密视频的地址。
- 视频加密：超级播放器可以播放加密视频（需要先设置Key防盗链），通过开发者服务器鉴权后生成的JWT给腾讯云服务器鉴权。

代码风格建议：
- 不要直接使用Key防盗链，而应在超级播放器SDK中播放视频，防止恶意爬虫直接获取连接以后获取原视频。
- 超级播放器签名必须经过开发者服务器鉴权以后发送，防止恶意爬虫绕过付费机制请求原视频。
"""

import base64
import hmac
import hashlib
import time
import random
from urllib.parse import urlparse, urlencode
from typing import Optional, Union

import jwt
from qcloud_vod.vod_upload_client import VodUploadClient
from qcloud_vod.model import VodUploadRequest
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.vod.v20180717 import vod_client, models

from django.conf import settings

from .base import call_qcloud_request
from qtutils.random import gen_random_str


# VOD云点播API根地址
VOD_API_ROOT = 'vod.tencentcloudapi.com'
# VOD云点播SDK
vod_sdk_client = VodUploadClient(settings.QCLOUD_SECRET_ID, settings.QCLOUD_SECRET_KEY)
# VOD客户端
cred = credential.Credential(settings.QCLOUD_SECRET_ID, settings.QCLOUD_SECRET_KEY)
httpProfile = HttpProfile()
httpProfile.endpoint = VOD_API_ROOT
clientProfile = ClientProfile()
clientProfile.httpProfile = httpProfile
VOD_CLIENT = vod_client.VodClient(cred, "", clientProfile)


# ----- API接口 -----

def call_vod_request(action, request_params, allowed_options=None):
    return call_qcloud_request(VOD_CLIENT, action, request_params, allowed_options)


def upload_media_file(name, region=None):
    """
    上传VOD媒体文件
    :param name:
    :param region:
    :return:
    """
    if region is None:
        region = settings.QCLOUD_PROJECT_REGION
    request = VodUploadRequest()
    request.MediaFilePath = name
    response = vod_sdk_client.upload(region, request)
    return response


def search_media_file_info(**request_params):
    """
    搜索VOD媒体文件信息
    :param request_params:
    :return:
    """
    return call_vod_request('SearchMedia', request_params)["MediaInfoSet"]


# ----- 工具函数：超级播放器SDK -----

def gen_decrypt_token(appid: Union[int, str], file_id: Union[int, str], expiration_second: Optional[int] = None) -> str:
    """
    生成超级播放器鉴权JWT，用于Key防盗链和加密视频的解密鉴权。
    详见：https://cloud.tencent.com/document/product/266/45554
    :param appid:
    :param file_id:
    :param expiration_second:
    :return:
    """
    if expiration_second is None:
        expiration_second = settings.QCLOUD_VOD_DECRYPT_TOKEN_EXPIRATION_SECOND
    current_timestamp = int(time.time())
    expire_timestamp = current_timestamp + int(expiration_second)
    # 用强制类型转换让payload格式符合要求
    payload = {
        "appId": int(appid),
        "fileId": str(file_id),
        "currentTimeStamp": int(current_timestamp),
        "expireTimeStamp": int(expire_timestamp),
        "pcfg": "basicDrmPreset",  # 重要：解密视频
        "urlAccessInfo": {
            't': hex(expire_timestamp)[2:],  # 特别注意：16进制小写字母，删去开头0x否则无法使用
            'exper': 0,
            'rlimit': 3,
            'us': gen_random_str(16)
        },
    }
    key = settings.QCLOUD_VOD_DEFAULT_KEY
    return jwt.encode(payload, key, algorithm='HS256').decode('utf-8')  # bytes转str


# ----- 工具函数：Key防盗链 -----

def gen_key_security_chain_url(raw_url, expire=3600, exper=0, rlimit=3):
    """
    生成Key防盗链URL。
    防盗链参数必须按照t、exper、rlimit、us、sign的顺序拼接。
    :return:
    """
    # 处理变量
    vod_dir = '/'.join(urlparse(raw_url).path.split('/')[:-1]) + '/'  # 特别注意：末尾需要带`/`，否则效验不通过
    t = str(hex(int(time.time())+int(expire)))[2:]  # 注意：最好删除0x开头以和腾讯云自己的签名生成工具保持一致
    exper = str(exper)
    rlimit = str(rlimit)
    us = gen_random_str(16)
    # 计算签名
    unhashed_sign = settings.QCLOUD_VOD_DEFAULT_KEY + vod_dir + t + exper + rlimit + us
    md5_instance = hashlib.md5()
    md5_instance.update(unhashed_sign.encode('utf-8'))
    sign = md5_instance.hexdigest()
    return raw_url + '?' + urlencode({'t': t, 'exper': exper, 'rlimit': rlimit, 'us': us, 'sign': sign})


# ----- 工具函数：客户端上传签名 -----

def gen_client_upload_sign(appid: Union[None, str, int] = None, expire: int = 3600):
    """
    客户端上传签名计算工具函数
    :param appid:
    :param expire:
    :return:
    """
    # 获取参数
    secret_id = settings.QCLOUD_SECRET_ID
    secret_key = settings.QCLOUD_SECRET_KEY
    if appid is None:
        appid = settings.QCLOUD_VOD_DEFAULT_APPID
    current_timestamp: int = int(time.time())
    expired_timestamp: int = current_timestamp + expire
    # 十进制数，最大值xxxxx（即32位无符号二进制数的最大值）
    random_value: int = random.randint(0, 999999)
    # 按照 URL QueryString 的格式要求拼接签名明文串original_sign
    # 将明文串original_sign使用UTF-8编码成字节数组
    original_sign = urlencode({
        'secretId': secret_id,
        'currentTimeStamp': current_timestamp,
        'expireTime': expired_timestamp,
        'random': random_value,
        'vodSubAppId': int(appid),
        'procedure': 'SimpleAesEncryptPreset',  # 默认设置AES加密模板
    }).encode('utf-8')
    # 用secret_key对明文串original_sign进行HMAC-SHA1加密
    encrypted_sign = hmac.new(secret_key.encode('utf-8'), original_sign, hashlib.sha1).digest()
    # 合并加密和未加密字符串，base64编码
    sign = base64.b64encode((encrypted_sign + original_sign))
    return sign
