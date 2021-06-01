# -*-coding: utf-8 -*-

import unittest
import os

from qcloud_sdk.sms.api import QCloudSMSAPIClient


class SMSAPITestCase(unittest.TestCase):
    def test_send_sms(self):
        client = QCloudSMSAPIClient()
        client.send_sms(phone_number_list=[os.environ.get('SMS_TEST_PHONE_NUMBER')],
                        app_id=os.environ.get('SMS_SDK_APP_ID'),
                        template_id=os.environ.get('SMS_TEMPLATE_ID'),
                        sign_name=os.environ.get('SMS_SIGN_NAME'),
                        template_param_list=['123456', '10'],
                        session_context='123456')


if __name__ == '__main__':
    unittest.main()
