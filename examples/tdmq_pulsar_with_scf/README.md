# 使用云函数的消息队列示例

使用云函数作为生产者和消费者的消息队列示例项目。

假设在项目根目录下运行命令行。

## 配置消息队列

1. 创建集群。
2. 创建命名空间。
3. 创建Topic。
4. 创建订阅。
5. 创建角色。
6. 命令空间配置角色。

## 配置环境变量

`.env`配置：

```
STAGE=
# 服务接入地址
PULSAR_SERVICE_URL=
# 已授权角色密钥
PULSAR_AUTHENTICATION=
# topic完整路径，格式为persistent://集群（租户）ID/命名空间/Topic名称，从【Topic管理】处复制
PULSAR_TOPIC=
# 订阅名称，如`sdk-demo`
PULSAR_SUBSCRIPTION_NAME=
```

Pulsar参数见：https://cloud.tencent.com/document/product/1179/56491

## 部署

```shell
cd examples/tdmq_pulsar_with_scf
scf deploy
```

如果没有登录，控制台会弹出二维码和登录链接。点击登录链接到网页扫码登录并授权即可。
（PS：二维码不确定是否可用。）

登录成功以后会在`.env`写入`TENCENT_APP_ID`、`TENCENT_SECRET_ID`、`TENCENT_SECRET_KEY`、`TENCENT_TOKEN`。

云端部署成功以后，需要切换到云端IDE下载requirements文件的依赖。

## 配置TDMQ触发器

必须在控制台手动配置。

1. 授权云函数角色。
2. 按照[文档](https://cloud.tencent.com/document/product/583/59102)配置。

## 运行

本地运行

```
scf invoke
```

或者在云端IDE运行。

## 监控

在"消息查询"页面查看消息轨迹可以看到消息的生产和消费情况。
