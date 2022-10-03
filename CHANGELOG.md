# CHANGELOG

## [v0.4.2] - 2022-07

（不兼容更新）增加对象存储API。

### Features

对象存储：
- 增加上传或更新对象API`put_object`。
- 增加删除对象API`delete_object`。
- 增加对象是否存在API`exists_object`。

### Refactored

对象存储：
- `request_cos_api`和`request_cos_bucket_api`增加`data`参数。
- （不兼容更新） `head_object`返回值改为`CosAPIResponse`对象。

## [v0.4.1] - 2022-06-01 

Hotfix版本。修复对象存储下载API异常。

### Refactored

- 重新定义Custom API为Integrated API，重命名所有相关类；Custom用于指代库的用户的自定义行为。

### Bugfix

对象存储：
- 下载对象API：修复下载文件未通过验证时删除异常。

## [v0.4.0] - 2022-05-03

### Features

APIClient:
- 增加`qcloud_api_client`单例，适用于环境变量传参的云原生应用。

日志服务：
- 增加日志服务基本API`request_cls_api`。
- 增加日志检索API`search_log`。

云函数：
- 增加云函数基本API`request_scf_api`。

机器翻译：
- 增加机器翻译基本API`request_tmt_api`。
- 增加文本翻译API`translate_text`


## [v0.3.6] - 2022-04-26

对象存储下载API增加断点续传功能。

### Features 

对象存储：
- `download_object_to_file`增加断点续传功能。

### Refactored

对象存储：
- 重构`CosAPIResponse`数据模型
- 重构API模块划分。

## [v0.3.5] - 2022-04-22 

### Refactored

对象存储：
- 重构CRC64算法以适应大文件计算。

### Bugfix 

- 修复`crcmod`配置异常。

## [v0.3.4] - 2022-04-22

### Bugfix

对象存储：
- 修复`download_object_to_file`效验异常。

### Removed 

- 移除`from qcloud_sdk import QCloudAPIClient`等的导入支持。

## [v0.3.3] - 2022-04-21

重构对象存储API。

### Features

对象存储：
- 增加数据模型`CosResponseData`。
- 增加HEAD Object API `head_object`。
- 增加自定义下载对象API`download_object_to_file`。

事件总线：
- `put_all_events`增加`time_sleep`投递休眠时间参数。
  
### Refactored 

对象存储：
- 重构底层API `request_cos_api`、`request_cos_bucket_api`。
- 重构GET Object API `get_object`。
- `get_cos_object`重命名为`get_object_storage_service`。

### Removed

对象存储：
- （不兼容更新）删除原下载对象API`get_object_to_file`。

## [v0.3.2] - 2022-04-16

修复事件总线API异常。

### Features

事件总线：
- 增加一次性所有投递事件的high-level API `put_all_events`

### Bugfix

事件总线：
- 事件投递API增加验证事件参数上限为10个。

## [v0.3.1] - 2022-03-28 

对象存储增加下载对象API。

## Features

对象存储：
- 增加`get_object`和`get_object_to_file`方法。

单元测试：
- 增加`QCLOUSDK_TEST_ALL`环境变量控制消耗云资源计费的单元测试。

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
