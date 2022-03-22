"""
云事件
"""

import json


class QCloudEvent(object):
    """
    云事件
    Defined by EB：https://cloud.tencent.com/document/api/1359/67704#Event

    TODO: 可考虑定义为dict或者defaultdict的子类型。
    """
    def __init__(self, source: str, type: str, subject: str, data: dict):
        self.source = source
        self.type = type
        self.subject = subject
        self.data = data

    def to_dict(self):
        return {
            "Source": self.source,
            "Type": self.type,
            "Subject": self.subject,
            "Data": json.dumps(self.data),
        }
