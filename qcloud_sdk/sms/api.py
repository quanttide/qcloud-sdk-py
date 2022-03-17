# -*- coding: utf-8 -*-
"""
腾讯云短信服务（SMS）云API
"""

from typing import Union, Optional

from qcloud_sdk.config import settings


class SmsAPIMixin(object):
    def request_sms_api(self, action: str, params: dict, region: Optional[str] = None, api_region: str = None):
        """
        请求SMS短信服务API

        :param action: API名称
        :param params: API参数
        :param region: 服务地域
        :param api_region: API接入地域
        :return:
        """
        region = region or settings.SMS_DEFAULT_REGION
        if not region:
            raise ValueError("地域（region）必填，请传入地域参数或设置QCLOUD_SMS_DEFAULT_REGION")
        # 请求API
        return self.request_api(service='sms', action=action, params=params, api_version='2021-01-11',
                                api_region=api_region, region=region,
                                supported_regions=settings.SMS_SUPPORTED_REGIONS,
                                supported_regions_doc=settings.SMS_SUPPORTED_REGIONS_DOC)

    # ----- 短信模板 -----
    def add_sms_template(self):
        """
        申请短信模板
        :return:
        """
        pass

    # --- 发送短信 ---
    def send_sms(self, phone_number_list: Union[list, tuple], app_id: Union[int, str], template_id: Union[int, str],
                 sign_name=None, template_param_list=None, extend_code=None,
                 session_context=None, sender_id=None, region=None):
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
        params = {'PhoneNumberSet': phone_number_list, 'SmsSdkAppId': app_id,
                  'TemplateId': template_id, 'SignName': sign_name,
                  'TemplateParamSet': template_param_list,
                  'SessionContext': session_context}
        # 短信码号扩展号，默认未开通，开通才可传参
        if extend_code:
            params['ExtendCode'] = extend_code
        # 国内短信无需填写该项；国际/港澳台短信已申请独立SenderId需要填写该字段，默认使用公共SenderId，无需填写该字段。
        if sender_id:
            params['SenderId'] = sender_id

        # 请求API
        data = self.request_sms_api('SendSms', params=params, region=region)["SendStatusSet"]
        # 返回结果
        return data

    def send_sms_to_single_user(self, phone_number, template_id, app_id, sign_name=None, template_param_list=None,
                                session_context=None, extend_code=None, sender_id=None, region=None):
        """
        向单个用户发送短信（自定义API）
        :return:
        """
        return self.send_sms(region=region, phone_number_list=[phone_number], template_id=template_id, app_id=app_id,
                             sign_name=sign_name, template_param_list=template_param_list, extend_code=extend_code,
                             session_context=session_context, sender_id=sender_id)[0]

    def pull_send_sms_status(self):
        """
        拉取回执
        :return:
        """
        pass
