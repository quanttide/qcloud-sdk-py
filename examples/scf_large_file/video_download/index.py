"""
下载视频
"""

import os

from qcloud_sdk.api import QCloudAPIClient


# 云函数传入环境变量使用CFS，本地使用项目根目录下data文件夹
LOCAL_ROOT_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
VIDEO_ROOT_PATH = os.environ.get('CFS_LOCAL_MOUNT_DIR', LOCAL_ROOT_PATH)


def download_video(object_key: str, file_path: str):
    """
    下载视频
    """
    client = QCloudAPIClient()
    client.download_object_to_file(object_key, file_path)


def main_handler(event, context):
    video_key = event['data']["video_key"]
    video_name = os.path.basename(video_key)
    file_path = os.path.join(VIDEO_ROOT_PATH, video_name)
    # 下载视频
    download_video(video_key, file_path)
    # 删除CFS缓存
    if os.path.exists(file_path):
        os.remove(file_path)
