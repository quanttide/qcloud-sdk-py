# -*- coding: utf-8 -*-
"""
腾讯云SMS短信服务API
"""

from typing import Union

from ..base.client import QCloudAPIClient


# 导入环境变量
from environs import Env
Env().read_env()


class QCloudSMSAPIClient(QCloudAPIClient):
    def __init__(self, secret_id=None, secret_key=None):
        super().__init__(secret_id, secret_key)
        self.service = 'sms'
        self.version = '2021-01-11'

    def request_sms_api(self, api, api_params, region=None):
        return super().request_api(self.service, api, api_params, region, self.version)

    def add_sms_template(self):
        """
        申请短信模板
        :return:
        """
        pass

    # --- 发送短信相关接口 ---
    def send_sms(self, phone_number_list: Union[list, tuple], app_id: Union[int, str], template_id: Union[int, str], sign_name=None,
                 template_param_list=None, extend_code=None, session_context=None, sender_id=None):
        """
        发送短信

        官方文档：
          - https://cloud.tencent.com/document/product/382/55981

        TODO:
          - 验证phone_number_list传入手机号格式是否正确、是否同为国内或者国外手机号。
          - 如果phone_number_list标记为国内，验证sign_name是否传入。
          - 补充参数文档
        """
        api_params = {'PhoneNumberSet': phone_number_list, 'SmsSdkAppid': app_id,
                      'TemplateID': template_id, 'SignName': sign_name,
                      'TemplateParamSet': template_param_list,
                      'ExtendCode': extend_code,
                      'SessionContext': session_context,
                      'SenderId': sender_id}
        data = self.request_sms_api('SendSms', api_params=api_params)
        return data["SendStatusSet"]

    def send_sms_to_single_user(self, phone_number, template_id, app_id, sign_name, template_param_list,
                                extend_code, session_context, sender_id):
        """
        向单个用户发送短信（自定义API）
        :return:
        """
        data = self.send_sms(phone_number_list=[phone_number], template_id=template_id, app_id=app_id,
                             sign_name=sign_name, template_param_list=template_param_list, extend_code=extend_code,
                             session_context=session_context, sender_id=sender_id)
        return data[0]

    def pull_send_sms_status(self):
        """
        拉取回执
        :return:
        """
        pass
