# qcloud-sdk-py

## 简介

量潮科技出品的腾讯云Python服务端SDK。

## 安装

```
pip install qcloud-sdk-py -i https://quanttide-pypi.pkg.coding.net/qtopen-python/qcloud-sdk-py/simple
```

## 使用

假设在环境变量中配置`QCLOUDSDK_SECRET_ID`和`QCLOUDSDK_SECRET_KEY`，未配置可以通过APIClient传入。
```python
# 导入模块
from qcloud_sdk.api import QCloudAPIClient

# 创建APIClient实例
client = QCloudAPIClient()

# 通用API
client.request_api(service='cvm', region='ap-shanghai', api='DescribeZones', api_params={})
```

## API列表

```python
# APIClient
from qcloud_sdk.api import QCloudAPIClient 

# 通用API
client = QCloudAPIClient()
client.request_api()

# COS对象存储API 
client.request_cos_api()
client.list_buckets()
client.list_objects()
client.list_all_objects()

# EB事件总线API
client.request_eb_api()
client.list_event_buses()
client.put_events()

# SMS短信服务API
client.request_sms_api()
client.send_sms_api()

# 配置
from qcloud_sdk.config import settings

# 数据模型
from qcloud_sdk.models import QCloudResource, QCloudEvent
from qcloud_sdk.scf.models import QCloudScfResource, QCloudScfEvent

# 异常类
from qcloud_sdk.exceptions import QCloudAPIException
```