# -*- coding: utf-8 -*-

import json
from typing import Optional

from tencentcloud.common.abstract_client import AbstractClient
from qcloud_sdk.base.exceptions import QcloudSdkException


def call_qcloud_request(client: AbstractClient, action: str, request_params: dict,
                        accepted_options: Optional[set] = None,
                        exception_class: Optional[QcloudSdkException] = None):
    if accepted_options is not None:
        assert request_params.keys() <= accepted_options, \
            '参数 {} 不在可接受列表中'.format(','.join(request_params.keys() - accepted_options))

    if exception_class is None:
        exception_class = QcloudSdkException

    body = client.call(action, request_params)
    response = json.loads(body)

    if 'Error' in response['Response']:
        raise exception_class(response['Response']['Error'])
    return response['Response']
