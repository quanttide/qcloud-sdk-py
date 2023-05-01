# 使用云函数的事件总线示例

以云函数为事件源和事件目标的事件总线示例。

## Step1: 下载代码到本地

```shell
git clone https://e.coding.net/quanttide/qtopen-python/qcloud-sdk-py.git
```

在命令行打开此用例根目录

```shell
cd <project_path>/examples/eb_with_scf
```

## Step2: 部署云函数到云端

手动操作如下。推荐使用流水线代替手动部署。

### Step2.1: 创建角色

为SCF创建一个可以访问EB的自定义角色，命名为`SCF_EBFullAccess`。

### Step2.2: 部署云函数

在`.env`文件配置如下环境变量：

```
TENCENT_SECRET_ID=<your-secret-id>
TENCENT_SECRET_KEY=<your-secret-key>
```

在本用例项目根目录运行

```shell
serverless deplpy
```

### Step2.2: 安装依赖

进入事件源函数的控制台，"函数代码"使用新版IDE进入。

注意：
- 旧版IDE无法进行下述进入终端操作。
- Python3.7暂不支持新版IDE。
- Safari无法使用新版IDE，一个经过大半年还没有修复的bug。

选择"终端">"新终端"。

切换到src文件夹

```shell
cd src
```

使用`pip`下载依赖
```shell
pip3 install -r requirements.txt -t .
```

注意不要使用`pip`，会使用系统内置的Python2的`pip`。

点击"部署"，然后"测试"，检查事件源是否可以正常运行。


## Step3: 手动配置事件总线

事件连接器是事件集的上游、事件目标是事件集的下游。依次配置即可。

### Step3.1: 创建事件集和事件连接器

在函数同地域（本用例为上海`ap-shanghai`）创建事件集。
- 事件集名称和事件集描述自定义。

点开事件集页面，创建事件连接器。
- 事件连接器名称自定义。
- 连接器类型选择API网关
- API服务类型选择新建
- API服务名称自定义。
- 请求方法选择`POST`
- 请求格式选择`http&https`
- API网关授权点确定

### Step3.2: 配置事件源发送消息到事件集

创建以后到API网关控制台页面，在"后端配置"的"事件集"获取事件集ID。 

切换到事件源函数，在"函数管理"的"函数配置"，设置环境变量：

```
QCLOUDSDK_EB_DEFAULT_EVENT_BUS_ID=<your-event-bus-id>
```


点击保存。

### Step3.3: 配置事件目标

事件总线控制台的"事件规则"，在刚创建的事件集下"新建事件规则"。
- 规则名称和规则描述自定义。
- 事件匹配选择"自定义"。
- 事件模式预览配置为SCF。

```json
{
  "source":"scf.cloud.tencent"
}
```

点击下一步，进入事件目标配置页面。

选择在Step2部署的事件目标函数。

## Step4: 手动运行事件源

回到事件源控制台，选择事件源函数，点击"测试"，确认运行成功。

切换到事件目标函数，选择"日志查询"，查看最新的记录，查看日志打印的event信息，可以看到事件被成功投递。

自此完成一轮配置。
