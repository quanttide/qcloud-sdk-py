# 腾讯云 Python SDK 

## 简介

量潮科技出品的腾讯云 Python SDK for Humans。

## 安装

推荐安装发布版：
```
pip install https://e.coding.net/quanttide/qtapps-python/qcloud-sdk-py.git@0.0.1
```

安装最新版本：
```
pip install https://e.coding.net/quanttide/qtapps-python/qcloud-sdk-py.git
```

## 使用

假设在环境变量中配置`TENCENT_SECRET_ID`和`TENCENT_SECRET_KEY`，未配置可以通过APIClient传入。
```
from qcloud_sdk import APIClient
client = APIClient()
client.request_api(service='cvm', region='ap-shanghai', api='DescribeZones', api_params={})
```