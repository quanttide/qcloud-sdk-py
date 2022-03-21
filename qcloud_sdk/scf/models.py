# -*- coding: utf-8 -*-

from qcloud_sdk.models import CloudResource


class ScfResource(CloudResource):
    def __init__(self, region, account, namespace, function_name):
        self.namespace = namespace
        self.function_name = function_name
        super().__init__(service_type='scf', region=region, account=account,
                         resource=f"namespace/{self.namespace}/function/{self.function_name}")
