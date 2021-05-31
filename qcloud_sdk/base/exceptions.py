# -*- coding: utf-8 -*-


class QCloudAPIException(Exception):
    def __init__(self, request_id, err_code, err_msg):
        self.request_id = request_id
        self.err_code = err_code
        self.err_msg = err_msg
