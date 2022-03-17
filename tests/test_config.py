"""
测试声明式配置导入和验证
"""

import unittest

from qcloud_sdk.config import settings


class DynaconfTestCase(unittest.TestCase):
    def test_load_settings(self):
        # 默认配置
        self.assertTrue(hasattr(settings, 'SMS_SUPPORTED_REGIONS'))
        # 环境变量
        self.assertTrue(hasattr(settings, 'SECRET_ID'))
        self.assertTrue(hasattr(settings, 'SECRET_KEY'))


if __name__ == '__main__':
    unittest.main()
