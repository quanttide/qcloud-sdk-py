# -*- coding: utf-8 -*-

from qcloud_sdk.config import settings


class ScfBaseAPIMixin(object):
    def request_scf_api(self, action, params, region=None):
        region = region or settings.SCF_DEFAULT_REGION or settings.DEFAULT_REGION
        if not region:
            raise ValueError('地域不可为空')
        return self.request_api(service='scf', action=action, params=params, region=region, api_version='2018-04-16')
