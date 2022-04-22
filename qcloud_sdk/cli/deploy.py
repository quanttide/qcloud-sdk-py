"""
部署命令

```shell
qcloud deploy
```
"""

import typer


cli = typer.Typer()


@cli.callback()
def main():
    return


if __name__ == '__main__':
    cli()
