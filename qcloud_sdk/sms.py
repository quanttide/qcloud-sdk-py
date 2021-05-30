# -*- coding: utf-8 -*-
"""
封装腾讯云SMS短信服务SDK
"""
from typing import Optional

from django.conf import settings
from django.core.cache import caches

from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile

from tencentcloud.sms.v20190711 import sms_client

from .base import QcloudSdkException, call_qcloud_request
from qtutils.random import gen_verification_code


# SMS客户端
CRED = credential.Credential(settings.QCLOUD_SECRET_ID, settings.QCLOUD_SECRET_KEY)
HTTP_PROFILE = HttpProfile()
HTTP_PROFILE.endpoint = "sms.tencentcloudapi.com"
CLIENT_PROFILE = ClientProfile()
CLIENT_PROFILE.httpProfile = HTTP_PROFILE
SMS_CLIENT = sms_client.SmsClient(CRED, settings.QCLOUD_PROJECT_REGION, CLIENT_PROFILE)


class QcloudSmsException(QcloudSdkException):
    pass


# ----- SDK二次封装 -----

def call_sms_request(action: str, request_params: dict, accepted_options: Optional[set] = None):
    return call_qcloud_request(SMS_CLIENT, action, request_params, accepted_options, QcloudSmsException)


def add_sms_template(request_params: dict) -> dict:
    """
    申请短信模板
    :return:
    """
    pass


def send_sms(**request_params) -> dict:
    """
    发送短信
    TODO：优化传参，处理必要参数和非必要参数
    :return:
    """
    accepted_options = {'PhoneNumberSet', 'TemplateID',
                        'SmsSdkAppid', 'Sign',
                        'TemplateParamSet', 'ExtendCode',
                        'SessionContext', 'SenderId'}
    response: dict = call_sms_request('SendSms', request_params, accepted_options)
    return response


def pull_send_sms_status():
    """
    拉取回执
    :return:
    """
    pass


# ----- 自定义SDK -----

def send_mobile_verification_code(mobile: str, code: Optional[str] = None,
                                  code_len: Optional[int] = None, timeout_minutes: int = 10,
                                  sandbox=False) -> str:
    """
    发送短信验证码
        - Status: 可用
        - TODO: 限制同一个手机号的使用频率

    :param mobile: 手机号，必填
    :param code: 验证码，默认自动生成，传入code时同时传入code_len时需要验证
    :param code_len: 验证码长度，默认为6位
    :param timeout_minutes:
    :param sandbox: 沙箱模式，默认为False
    :return: SessionContext参数设置的验证码
        示例：
          {
            "SerialNo": "5000:104571066915705365784949619",
            "PhoneNumber": "+8618511122233",
            "Fee": 1,
            "SessionContext": "test",
            "Code": "Ok",
            "Message": "send success",
            "IsoCode": "CN"
          }
    """
    # 国内手机号处理
    mobile = '+86' + mobile

    # 生成验证码
    if code is None:
        # 生成或者验证随机验证码，默认6位
        if code_len is None:
            code_len = 6
        code: str = gen_verification_code(code_len)
    else:
        if code_len is not None:
            assert len(code) == code_len, "输入验证码和输入验证码长度不一致"

    # 手机号，验证码和有效时间作为模板参数传入
    # 参考：
    #   - SMS API: https://cloud.tencent.com/document/product/382/38778
    #   - SMS Python SDK: https://cloud.tencent.com/document/product/382/43196
    request_params = {
        'SmsSdkAppid': '1400392220',
        'Sign': '量潮科技',
        'PhoneNumberSet': [mobile],
        'TemplateID': '650873',
        'TemplateParamSet': [code, timeout_minutes],
        'SessionContext': code,
    }

    # 发送请求，沙箱模式下仅模拟输出
    # response数据示例：
    #       {
    #         "SerialNo": "5000:104571066915705365784949619",
    #         "PhoneNumber": "+8618511122266",
    #         "Fee": 1,
    #         "SessionContext": "test",
    #         "Code": "Ok",
    #         "Message": "send success",
    #         "IsoCode": "CN"
    #       }
    if not sandbox:
        response: dict = send_sms(**request_params)["SendStatusSet"][0]
    else:
        response = {
            'Code': 'Ok',
            'SessionContext': request_params['SessionContext'],
        }

    if response['Code'] == 'Ok':
        # 把数据缓存到专门储存验证码的表中，设置过期时间
        cache = caches['code']
        cache.set(mobile, response['SessionContext'], timeout=60 * timeout_minutes)  # Bug: 有数据
        return response['SessionContext']
    else:
        raise QcloudSmsException(response)
