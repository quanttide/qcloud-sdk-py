"""
列举对象列表示例
"""

from qcloud_sdk.api import QCloudAPIClient


def list_all_object_names():
    client = QCloudAPIClient()
    data = client.list_all_objects()
    return [item['Key'] for item in data]


def main_handler(event, context):
    object_names = list_all_object_names()
    print(f'对象数量有{len(object_names)}个')
    return object_names
