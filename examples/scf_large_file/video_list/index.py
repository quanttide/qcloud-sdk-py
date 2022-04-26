"""
生成视频文件列表
"""

from typing import List, Dict, Any

from qcloud_sdk.api import QCloudAPIClient
from qcloud_sdk.scf.models import QCloudScfEvent


def list_video_files() -> List[Dict[str, Any]]:
    client = QCloudAPIClient()
    data = client.list_all_objects()
    # 过滤符合规范的视频文件
    results = []
    for item in data:
        if '.mp4' in item['Key']:
            results.append({'video_key': item['Key'], 'size': int(item['Size']) or 0})
    return results


def put_video_task_events(tasks):
    event_list = [QCloudScfEvent(task) for task in tasks]
    client = QCloudAPIClient()
    client.put_all_events(event_list, time_sleep=1)


def main_handler(event, context):
    tasks = list_video_files()
    # 选择最大的20个视频
    selected_tasks = sorted(tasks, key=lambda item: item['size'], reverse=True)[0:20]
    put_video_task_events(selected_tasks)
