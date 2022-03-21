# 腾讯云 Python SDK 

## 简介

量潮科技出品的腾讯云 Python SDK for Humans。

## 安装

```
pip install qcloud-sdk-py -i 
```


## 使用

假设在环境变量中配置`QCLOUD_SECRET_ID`和`QCLOUD_SECRET_KEY`，未配置可以通过APIClient传入。
```python
# 导入模块
from qcloud_sdk import APIClient as QCloudAPIClient

# 创建APIClient实例
client = QCloudAPIClient()

# 通用API
client.request_api(service='cvm', region='ap-shanghai', api='DescribeZones', api_params={})
```

## API列表

```python
# APIClient
from qcloud_sdk import APIClient as QCloudAPIClient 

# 通用API
client = QCloudAPIClient()
client.request_api()

# 事件总线API
client.request_eb_api()
client.list_event_buses()
client.put_events()

# 短信服务
client.request_sms_api()
client.send_sms_api()

# 数据模型
from qcloud_sdk.models import CloudResource
from qcloud_sdk.scf.models import ScfResource
from qcloud_sdk.eb.models import CloudEvent

# 异常类
from qcloud_sdk.exceptions import QCloudAPIException
```