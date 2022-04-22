"""
腾讯云SDK命令行工具

```shell
qcloud <command> <subcommand> <params>
```

本地开发调试
```shell
python3 qcloud_sdk/cli --help
```

TODO：
  - 修复本地终端导入qcloud_sdk其他模块报错
  - 命令行文档对列举的可用命令分类整理为DevOps命令和云服务命令两类。

参考资料：
  - https://typer.tiangolo.com
  - https://typer.tiangolo.com/typer-cli/
  - https://mp.weixin.qq.com/s/h1Avhk6FuX375PIySvsqIQ
"""
import typer

from qcloud_sdk.cli.deploy import cli as deploy_cli
from qcloud_sdk.scf.cli import cli as scf_cli


# Typer实例
cli = typer.Typer()
# 添加子命令
# https://typer.tiangolo.com/tutorial/subcommands/add-typer/

# DevOps命令
cli.add_typer(deploy_cli, name='deploy')

# 云服务命令
cli.add_typer(scf_cli, name='scf')


if __name__ == '__main__':
    cli()
