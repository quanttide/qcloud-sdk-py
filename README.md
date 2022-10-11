# qcloud-sdk-py

## 简介

量潮科技出品的腾讯云Python服务端SDK。

## 安装

```
pip install qcloud-sdk-py
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

## 文档

[腾讯云Python服务端SDK文档](https://quanttide.github.io/qcloud-sdk-py/README.html)