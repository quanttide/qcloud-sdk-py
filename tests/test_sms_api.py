# -*-coding: utf-8 -*-

import unittest

from qcloud_sdk.exceptions import QCloudAPIException
from qcloud_sdk.config import settings

from tests.client import APIClientTestCase


class SmsAPITestCase(APIClientTestCase):
    def setUp(self):
        self.session_context = '123456'

    @unittest.skipUnless(settings.TEST_ALL, '避免发送真实短信验证码')
    def test_send_sms(self):
        data = self.client.send_sms(
            phone_number_list=[settings.SMS_TEST_PHONE_NUMBER],
            app_id=settings.SMS_SDK_APP_ID,
            template_id=settings.SMS_TEMPLATE_ID,
            sign_name=settings.SMS_SIGN_NAME,
            template_param_list=['123456', '10'],
            session_context=self.session_context
        )
        self.assertTrue(data)

    @unittest.skipUnless(settings.TEST_ALL, '避免发送真实短信验证码')
    def test_send_sms_to_single_user(self):
        data = self.client.send_sms_to_single_user(
            phone_number=settings.SMS_TEST_PHONE_NUMBER,
            app_id=settings.SMS_SDK_APP_ID,
            template_id=settings.SMS_TEMPLATE_ID,
            sign_name=settings.SMS_SIGN_NAME,
            template_param_list=['123456', '10'],
            session_context=self.session_context
        )
        self.assertEqual(data['SessionContext'], self.session_context)

    @unittest.skip('待重新实现异常处理')
    def test_send_sms_to_single_user_with_error_sign_name(self):
        with self.assertRaises(QCloudAPIException) as e:
            data = self.client.send_sms_to_single_user(
                phone_number=settings.SMS_TEST_PHONE_NUMBER,
                app_id=settings.SMS_SDK_APP_ID,
                template_id=settings.SMS_TEMPLATE_ID,
                sign_name="错误的签名",
                template_param_list=['123456', '10'],
                session_context=self.session_context
            )
        self.assertEqual(e.exception.err_code, 'FailedOperation.SignatureIncorrectOrUnapproved')


if __name__ == '__main__':
    unittest.main()
