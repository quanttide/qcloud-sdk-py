"""
声明式配置

从环境变量导入：
- 用户配置通过环境变量`QCLOUD_SDK`前缀传入。
- 云函数运行环境默认配置内置环境变量。

TODO：
- 具体配置方案还需要反复通过用例打磨，请开发者们特别注意收集各种传参用例。

参考资料：
  - https://www.dynaconf.com
  - 云函数环境变量：https://cloud.tencent.com/document/product/583/30228
"""

import os

from dynaconf import Dynaconf


# 默认配置文件
default_settings_files = ['settings.toml']
# 云函数运行环境
if os.environ.get('TENCENTCLOUD_RUNENV') == 'SCF':
    default_settings_files.append('scf/settings.toml')
# 合并默认配置
default_settings_files = [os.path.join(os.path.dirname(__file__), settings_file) for settings_file in default_settings_files]

# 声明式配置实例
settings = Dynaconf(
    settings_files=default_settings_files,
    environments=True,
    envvar_prefix='QCLOUDSDK',
    load_dotenv=True,
)
