"""
事件源示例
"""

from qcloud_sdk import QCloudAPIClient
from qcloud_sdk.scf.models import QCloudScfEvent

# 单例
client = QCloudAPIClient()


def put_events():
    event = QCloudScfEvent(data={'task_id': '1'})
    client.put_events(event_list=[event.to_dict()])


def main_handler(event, context):
    return put_events()
