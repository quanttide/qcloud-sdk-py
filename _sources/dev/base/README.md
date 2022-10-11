# 基础模块

这部分主要的目标是重构官方SDK（`tencentcloud-sdk-python`）的`common`文件夹。

## 官方SDK源码结构分析

`common`由以下几个Python包和模块构成：
- `abstract_model.py`: 提供了一个基础抽象类，本项目内其他类都从这里继承。
- `abstract_client.py`: 提供了一个API客户端抽象类。
- `common_client.py`: 提供了抽象类的接口，其他模块的API客户端从此调用或继承。
- `credentials.py`: 提供了云API密钥类，作为参数传入API客户端。
- `sign.py`: API签名算法。
- `profile`: 提供了一些API访问的公共参数。
  - `http_profile.py`: 提供了HTTP协议相关的参数。
  - `client_profile.py`: 上述文件加上其他辅助参数。
- `http`: 提供了HTTP请求工具。
- `exception`: 异常类。

熟悉Java的同学大概可以从源码感觉到，这个项目有非常浓厚的Java或者Objective-C的痕迹，因此有分离出抽象类的写法。
对于这个Python项目来说，这是完全没有必要的，直接通过传参给API即可为不同的云服务定制接口，抽象类是不必要的冗余写法，
因此`abstract_client.py`和`common_client.py`是可以合并的。

`abstract_model`类提供了JSON数据序列化和反序列化成Python对象的方法，从其他地方的调用看，这里主要是加工参数方便传入，
可能开发者不熟悉Python的函数有func(**kwargs)的传参方法。

`http`提供了HTTP请求工具，这个开发者大概是不知道Python有一个叫做`requests`的库，完全是一个没用的包。

`credentials.py`模块和`profile`包都作为API的公共参数传入，而且大部分情况下开发者并不需要设置他们，
基于Python函数的默认参数实现即可，完全可以直接作为APIClient类参数传入。

因此，官方API调用示例是：
```
from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.cvm.v20170312 import cvm_client, models
try:
    cred = credential.Credential("secretId", "secretKey")
    client = cvm_client.CvmClient(cred, "ap-shanghai")
    req = models.DescribeInstancesRequest()
    resp = client.DescribeInstances(req)
    print(resp.to_json_string())
except TencentCloudSDKException as err:
    print(err)
```

这还是简化版，详细版又臭又长，这里不再引用，代码详见：https://cloud.tencent.com/document/sdk/Python。


## 重构方案

基于上面的分析，我们实际上只需要在我们的`base`文件夹下实现这几个模块：
- `client.py`: 实现一个公共APIClient类，允许传入云API密钥和设置公共参数。
- `sign.py`: 实现API的签名算法，使用工厂方法的设计模式封装不同版本的API签名，被`client.py`调用。
- `exceptions.py`: 实现一个公共Exception类，处理API接口返回的异常。

并且把这些模块在项目根目录的`__init.py__`中导入。

经过我们的重构以后，导入和调用方式可以大幅简化为：
```
from qcloud_sdk import QCloudAPIClient, QCloudSDKException
try:
    client = CloudAPIClient(secret_id='', secret_key='', other_param='some_value')
    data = client.call_some_api('api_name', **{'param1': 'value1'})
except QCloudSDKException as e:
    print(e)
```
