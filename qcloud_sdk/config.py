"""
声明式配置

参考资料：
  - https://www.dynaconf.com
"""

import os

from dynaconf import Dynaconf


# 默认配置文件
default_settings_file = os.path.join(os.path.dirname(__file__), 'settings.toml')

# 声明式配置实例
settings = Dynaconf(
    settings_file=default_settings_file,
    environments=True,
    envvar_prefix='QCLOUD',
    load_dotenv=True,
)
