# -*-coding: utf-8 -*-

import unittest
import os

from qcloud_sdk.sms.api import QCloudSMSAPIClient
from qcloud_sdk.sms.exception import QCloudSMSAPIException

# 导入环境变量
from environs import Env
Env().read_env()


class SMSAPITestCase(unittest.TestCase):
    @classmethod
    def setUp(cls):
        cls.client = QCloudSMSAPIClient()

    def test_send_sms(self):
        data = self.client.send_sms(
            phone_number_list=[os.environ.get('SMS_TEST_PHONE_NUMBER')],
            app_id=os.environ.get('SMS_SDK_APP_ID'),
            template_id=os.environ.get('SMS_TEMPLATE_ID'),
            sign_name=os.environ.get('SMS_SIGN_NAME'),
            template_param_list=['123456', '10'],
            session_context='123456'
        )

    def test_send_sms_to_single_user(self):
        session_context = '123456'
        data = self.client.send_sms_to_single_user(
            phone_number=os.environ.get('SMS_TEST_PHONE_NUMBER'),
            app_id=os.environ.get('SMS_SDK_APP_ID'),
            template_id=os.environ.get('SMS_TEMPLATE_ID'),
            sign_name=os.environ.get('SMS_SIGN_NAME'),
            template_param_list=['123456', '10'],
            session_context=session_context
        )
        self.assertEqual(data['SessionContext'], session_context)

    def test_send_sms_to_single_user_with_error_sign_name(self):
        session_context = '123456'

        with self.assertRaises(QCloudSMSAPIException) as e:
            data = self.client.send_sms_to_single_user(
                phone_number=os.environ.get('SMS_TEST_PHONE_NUMBER'),
                app_id=os.environ.get('SMS_SDK_APP_ID'),
                template_id=os.environ.get('SMS_TEMPLATE_ID'),
                sign_name="错误的签名",
                template_param_list=['123456', '10'],
                session_context=session_context
            )
        self.assertEqual(e.exception.err_code, 'FailedOperation.SignatureIncorrectOrUnapproved')


if __name__ == '__main__':
    unittest.main()
