"""
列举对象列表示例
"""

from qcloud_sdk.api import QCloudAPIClient


def main_handler(event, context):
    client = QCloudAPIClient()
    data = client.list_all_objects()
    # 列举对象Key
    object_names = [item['Key'] for item in data]
    print(f'对象数量有{len(object_names)}个')
    # 选取最大文件
    # https://www.programiz.com/python-programming/methods/built-in/max
    max_file = max(data, key=lambda item: int(item['Size']) if item['Size'] else 0)
    print(f'最大文件为{max_file["Key"]}')
