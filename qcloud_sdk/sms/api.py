# -*- coding: utf-8 -*-
"""
腾讯云SMS短信服务API
"""

from typing import Union

from ..base.client import QCloudAPIClient
from .exception import QCloudSMSAPIException


class QCloudSMSAPIClient(QCloudAPIClient):
    def __init__(self, secret_id=None, secret_key=None, region: str = 'ap-guangzhou'):
        super().__init__(secret_id, secret_key)
        self.service = 'sms'
        self.api_version = '2021-01-11'
        # 可选地域：https://cloud.tencent.com/document/api/382/52071#.E5.9C.B0.E5.9F.9F.E5.88.97.E8.A1.A8
        assert region in ['ap-guangzhou', 'ap-nanjing']
        self.region = region

    def request_sms_api(self, api: str, api_params: dict):
        """
        请求SMS短信服务API

        :param api: API名称
        :param api_params: API参数
        :return:
        """
        return super().request_api(service=self.service, api=api, api_params=api_params, region=self.region, api_version=self.api_version)

    def add_sms_template(self):
        """
        申请短信模板
        :return:
        """
        pass

    # --- 发送短信相关接口 ---
    def send_sms(self, phone_number_list: Union[list, tuple], app_id: Union[int, str], template_id: Union[int, str],
                 sign_name=None, template_param_list=None, extend_code=None,
                 session_context=None, sender_id=None):
        """
        发送短信

        官方文档：
          - https://cloud.tencent.com/document/product/382/55981

        TODO:
          - 验证phone_number_list传入手机号格式是否正确、是否同为国内或者国外手机号。
          - 如果phone_number_list标记为国内，验证sign_name是否传入。
          - 补充参数文档
          - （重要）处理返回结果中的业务错误码，详见：https://cloud.tencent.com/document/api/382/52075#.E4.B8.9A.E5.8A.A1.E9.94.99.E8.AF.AF.E7.A0.81
        """
        # API接口参数
        api_params = {'PhoneNumberSet': phone_number_list, 'SmsSdkAppId': app_id,
                      'TemplateId': template_id, 'SignName': sign_name,
                      'TemplateParamSet': template_param_list,
                      'SessionContext': session_context}
        # 短信码号扩展号，默认未开通，开通才可传参
        if extend_code:
            api_params['ExtendCode'] = extend_code
        # 国内短信无需填写该项；国际/港澳台短信已申请独立SenderId需要填写该字段，默认使用公共SenderId，无需填写该字段。
        if sender_id:
            api_params['SenderId'] = sender_id

        # 请求API
        data = self.request_sms_api('SendSms', api_params=api_params)["SendStatusSet"]
        # 返回结果
        return data

    def send_sms_to_single_user(self, phone_number, template_id, app_id, sign_name=None, template_param_list=None,
                                session_context=None, extend_code=None, sender_id=None):
        """
        向单个用户发送短信（自定义API）
        :return:
        """
        data = self.send_sms(phone_number_list=[phone_number], template_id=template_id, app_id=app_id,
                             sign_name=sign_name, template_param_list=template_param_list, extend_code=extend_code,
                             session_context=session_context, sender_id=sender_id)[0]
        # 处理异常
        if data['Code'] != 'Ok':
            raise QCloudSMSAPIException(data['Code'], data['Message'])
        return data

    def pull_send_sms_status(self):
        """
        拉取回执
        :return:
        """
        pass
