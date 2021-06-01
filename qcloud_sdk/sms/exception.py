# -*- coding: utf-8 -*-


class QCloudSMSAPIException(Exception):
    def __init__(self, err_code, err_msg):
        self.err_code = err_code
        self.err_msg = err_msg

    def __str__(self):
        return f"\n - sms error code: {self.err_code}\n - sms error message: {self.err_msg}"
