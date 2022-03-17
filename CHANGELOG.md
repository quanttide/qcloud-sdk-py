# CHANGELOG

## [v0.1.0] - 2022-03-17 

腾讯云基本APIClient，SMS短信服务基本API。

### Features

通用：
- 基于通用API规则实现的`BaseAPIClient`及其签名算法。
- 基于dynaconf的声明式配置`settings`实例。
- 异常类`QCloudAPIException`。

云产品：
- SMS短信服务：
  - 基本API。
  - 发送短信API。