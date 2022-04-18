# -*- coding: utf-8 -*-

import importlib


def reload_settings() -> None:
    """
    强制重载模块，从环境变量重新生成settings
    """
    from qcloud_sdk import config
    importlib.reload(config)


