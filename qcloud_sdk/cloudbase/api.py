# -*- coding: utf-8 -*-

from qcloud_sdk.base.client import QCloudAPIClient
from qcloud_sdk.base.sign import cal_auth


class CloudBaseAPIClient(QCloudAPIClient):
    """
    云开发用户API
    """
    def __init__(self, secret_id=None, secret_key=None, region: str = 'ap-guangzhou'):
        super().__init__(secret_id, secret_key)
        self.service = 'tcb'
        self.host = 'tcb-api.tencentcloudapi.com'
        self.api_version = '1.0'

    def gen_request_headers(self, endpoint, api, api_params, timestamp, service=None, api_version=None, region=None):
        if service is None:
            service = self.service
        if api_version is None:
            api_version = self.api_version
        headers = {
            'content-type': 'application/json',
            'X-CloudBase-Authorization': api_version + " " + cal_auth(self.secret_id, self.secret_key, endpoint, service, api_params, timestamp),
            'X-CloudBase-SessionToken': '',
            'X-CloudBase-TimeStamp': timestamp,
        }
        return headers

    def request_cloudbase_api(self, api, api_params):
        api_url = self.host  # TODO: 拼接URL
        return self.request_api(service=self.service, api=api, api_params=api_params, endpoint=api_url, api_version=self.api_version)

