# CHANGELOG

## [v0.3.0] - 2022-03-25

增加对象存储API。

## Features

对象存储：
- 增加对象存储基本客户端Mixin类`qcloud_sdk.cos.client.CosBaseAPIClientMixin`及通用API`request_cos_api`。
- 增加对象存储GET Service(List Buckets) API、GET Bucket(List Objects) API。
- 增加high-level API 列举存储桶下所有对象`list_all_objects`。
- 增加对象存储签名算法`qcloud_sdk.cos.sign`模块。


## [v0.2.3] - 2022-03-24

增加投递单个事件API。

## Features

通用：
- 增加云事件列表数据模型`QCloudEventList`。

事件总线：
- 增加投递单个事件API`put_event`。

## Refactored

事件总线：
- 使用`QCloudEventList`重构投递事件`put_events`内部实现。


## [v0.2.2] - 2022-03-23

增加临时密钥支持

## Features

通用：
- `APIClientInitializer`支持临时密钥初始化

单元测试：
- 增加测试工具函数`reload_settings`。


## [v0.2.1] - 2022-03-22 

优化事件总线和云函数相关实现。

## Features

云函数：
- 使用运行环境内置环境变量作为SDK默认参数。
- 增加`QCloudScfEvent`数据模型，在云函数运行环境里默认本云函数为事件源。

事件总线：
- 增加基于云函数的事件总线用例。

## Refactor

通用：
- 使用CloudEvent官方SDK重构云事件数据模型`QCloudEvent`
- 公开API重命名，增加QCloud。
- 修改环境变量前缀为`QCLOUDSDK`以避免云函数环境变量限制。

云函数：
- `QCloudScfResource`简化传参。

## Bugfix

- setup.cfg增加package_data设置、修复package.find的exclude选项。


## [v0.2.0] - 2022-03-21

云资源`CloudResource`和云事件`CloudEvent`数据模型，EB事件总线API。

### Features

通用：
  - 云资源数据模型 `models.CloudResource`。

事件总线：
  - 基本API `APIClient.request_eb_api`。
  - 列举事件总线API `APIClient.list_event_buses`。
  - 事件投递API `APIClient.put_events`。
  - 云事件数据模型 `eb.models.CloudEvent`。

云函数：
  - 云函数资源数据模型`scf.models.ScfResource`。


## [v0.1.0] - 2022-03-17 

腾讯云基本APIClient，SMS短信服务基本API。

### Features

通用：
  - 基于通用API规则实现的`BaseAPIClient`及其签名算法。
  - 基于dynaconf的声明式配置`settings`实例。
  - 异常类`QCloudAPIException`。

SMS短信服务：
  - 基本API `APIClient.request_sms_api`。
  - 发送短信API `APIClient.send_sms`。
