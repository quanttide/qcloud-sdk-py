# -*- coding: utf-8 -*-

from qcloud_sdk.models.resources import QCloudResource
from qcloud_sdk.models.events import QCloudEvent
from qcloud_sdk.config import settings


class QCloudScfResource(QCloudResource):
    """
    云函数资源
    """
    def __init__(self,  namespace=None, function_name=None, region=None, account=None):
        self.namespace = namespace or settings.SCF_DEFAULT_NAMESPACE
        assert self.namespace, 'namespace不可为空'
        self.function_name = function_name or settings.SCF_DEFAULT_FUNCTION_NAME
        assert self.function_name, 'function_name不可为空'
        super().__init__(
            service_type='scf', region=region, account=account,
            resource=f"namespace/{self.namespace}/function/{self.function_name}",
        )


class QCloudScfEvent(QCloudEvent):
    """
    云函数事件
    """
    def __init__(self, data, **attributes):
        attributes['source'] = attributes.get('source') or 'scf.cloud.tencent'
        attributes['subject'] = attributes.get('subject') or QCloudScfResource().to_string()
        attributes['type'] = attributes.get('type') or ''
        super().__init__(data, **attributes)
