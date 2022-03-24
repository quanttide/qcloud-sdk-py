"""
事件源示例
"""

from qcloud_sdk.api import QCloudAPIClient
from qcloud_sdk.scf.models import QCloudScfEvent


def put_events():
    event = QCloudScfEvent(data={'task_id': '1'})
    client = QCloudAPIClient()
    client.put_event(event=event)


def main_handler(event, context):
    return put_events()
