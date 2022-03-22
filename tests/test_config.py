"""
测试声明式配置导入和验证
"""

import os
import unittest
from unittest import mock
import importlib


class DynaconfTestCase(unittest.TestCase):
    """
    TODO：
      - 充分讨论各种可能的导入方法，把导入配置和使用配置彻底解耦。
      - 从测试必须强制重载（setUp都不可以）的实现来看，目前的实现并不理想，最好是可以使用Dynaconf的机制判断和导入云函数环境变量。
    """
    def test_load_settings(self):
        # 强制重载模块后重新导入
        from qcloud_sdk import config
        importlib.reload(config)
        from qcloud_sdk.config import settings
        # 默认配置
        self.assertTrue(hasattr(settings, 'SMS_SUPPORTED_REGIONS'))
        # 环境变量
        self.assertTrue(hasattr(settings, 'SECRET_ID'))
        self.assertTrue(hasattr(settings, 'SECRET_KEY'))

    @mock.patch.dict(os.environ, {
        'TENCENTCLOUD_RUNENV': 'SCF',
        'TENCENTCLOUD_SECRET_ID': 'fake-secret-id',
        'TENCENTCLOUD_SECRET_KEY': 'fake-secret-key',
        'TENCENTCLOUD_UIN': 'fake-uid',
        'TENCENTCLOUD_APPID': 'fake-appid',
        'TENCENTCLOUD_REGION': 'fake-region',
        'SCF_RUNTIME': 'fake-scf-runtime',
        'SCF_FUNCTIONNAME': 'fake-scf-function-name',
    })
    def test_load_settings_scf_runtime(self):
        # 强制重载模块后重新导入
        from qcloud_sdk import config
        importlib.reload(config)
        from qcloud_sdk.config import settings
        # 云函数运行环境内置配置取代SDK默认配置
        self.assertEqual('SCF', os.environ['TENCENTCLOUD_RUNENV'])
        self.assertEqual('fake-scf-runtime', settings.SCF_RUNTIME)
        self.assertEqual('fake-scf-runtime', settings.scf_runtime)
        # 云函数运行环境的配置会被用户配置取代
        self.assertEqual(os.environ.get('QCLOUD_SDK_SECRET_ID'), settings.SECRET_ID)


if __name__ == '__main__':
    unittest.main()
