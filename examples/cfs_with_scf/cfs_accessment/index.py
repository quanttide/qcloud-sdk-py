# -*- coding: utf-8 -*-

import os


CFS_PATH = os.environ.get('CFS_LOCAL_MOUNT_DIR')


def main_handler(event, context):
    for i in os.listdir(CFS_PATH):
        print(i)
        os.remove(os.path.join(CFS_PATH, i))
    return "文件系统已经清空"
