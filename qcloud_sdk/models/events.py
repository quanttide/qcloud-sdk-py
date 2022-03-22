"""
云事件
"""

import string
import json

from cloudevents.http import CloudEvent


class QCloudEvent(CloudEvent):
    """
    云事件
    Defined by EB：https://cloud.tencent.com/document/api/1359/67704#Event
    """
    def __init__(self, data: dict, **attributes):
        super().__init__(attributes, data)

    def to_dict(self):
        """
        TODO: 支持dict工厂方法；重构成更Pythonic的实现。
        :return:
        """
        # attributes的key转大写
        return_data = {}
        for key, value in self._attributes.items():
            # 目前API只支持这几个字段传入
            if key in ['source', 'type', 'subject']:
                return_data[key.capitalize()] = value
        # data的value转json
        return_data['Data'] = json.dumps(self.data)
        return return_data
