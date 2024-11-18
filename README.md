<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="https://img.picui.cn/free/2024/10/28/671f78556a9ee.png" width="180" height="180" alt="NoneBotPluginLogo"></a>

# nonebot-plugin-manageweb

_✨nb商店插件安装器web版✨_

<a href="https://github.com/CM-Edelweiss/nonebot-plugin-manageweb">
    <img alt="Image Size" src="https://img.shields.io/pypi/dm/nonebot-plugin-manageweb">
    <img alt="Image Size" src="https://img.shields.io/pypi/v/nonebot-plugin-manageweb">
</a>

</div>

## 📖 介绍

使用webui安装、更新、卸载插件和修改`.evn.*`文件，并提供webui接入支持<br>
对非电脑和手机用户不友好，可能出现错位<br>
（~~我是css低手~~）

## 💿 安装


> [!WARNING]
> 该插件需要fastapi支持

`使用镜像站可能需要等待镜像站同步`

<details open>
<summary>使用 nb-cli 安装</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

    nb plugin install nonebot-plugin-manageweb

</details>

<details>
<summary>使用包管理器安装</summary>
在 nonebot2 项目的插件目录下, 打开命令行, 根据你使用的包管理器, 输入相应的安装命令

<details>
<summary>pip</summary>

    pip install nonebot-plugin-manageweb
</details>
<details>
<summary>pdm</summary>

    pdm add nonebot-plugin-manageweb
</details>
<details>
<summary>poetry</summary>

    poetry add nonebot-plugin-manageweb
</details>
<details>
<summary>conda</summary>

    conda install nonebot-plugin-manageweb
</details>

打开 nonebot2 项目根目录下的 `pyproject.toml` 文件, 在 `[tool.nonebot]` 部分追加写入

    plugins = ["nonebot_plugin_manageweb"]

</details>

## 📋 效果
```
webui默认地址ip:端口/mw/login
```
<details>
<summary>webui效果</summary>

![_](https://img.picui.cn/free/2024/11/17/6739b4f8a3b17.png)
![_](https://img.picui.cn/free/2024/11/17/6739b4f90f618.png)
![_](https://img.picui.cn/free/2024/11/17/6739b4f861f03.png)
![_](https://img.picui.cn/free/2024/11/17/6739b4f73bd4a.png)

</details>

## ⚙️ 配置

在 nonebot2 项目的`.env`文件中添加下表中的必填配置

| 配置项 | 必填 | 默认值 | 说明 |
|:-----:|:----:|:----:|:----:|
| mw_username| 否 | admin |后台管理用户名 |
| mw_password| 否 | admin | 后台管理密码 |
| mw_key| 否 | ... | 后台管理token密钥 |


## 🎉 接入webui（未验证）
- api接入
> 使用此方法访问地址未/mw/api/xxx
> 也可以自行创建
```python
自行创建
from nonebot_plugin_manageweb.utils import authentication
from nonebot import get_app, get_driver
DRIVER = get_driver()

@DRIVER.on_startup
async def web():
    app: FastAPI = get_app()

    @app.post("/mw/api/xxx", response_class=JSONResponse, dependencies=[authentication()])
    async def _(user: UserModel):
        pass
```

```python
api接入
from nonebot_plugin_manageweb.web import BaseApiRouter
from nonebot_plugin_manageweb.utils import authentication
from fastapi import APIRouter
from fastapi.responses import JSONResponse


route = APIRouter()

@route.post(
    '/xxx', response_class=JSONResponse, dependencies=[authentication()]
)
async def _():
    pass

#添加api到BaseApiRouter
BaseApiRouter.include_router(home_route)
```

- amis界面添加
```python
from amis import (
    PageSchema,
    Page,
    ....
)
from nonebot_plugin_manageweb.utils import background_css #背景图css
from nonebot_plugin_manageweb.page.main import admin_app

xxx_page = PageSchema(url='/地址', icon='图标', label='页面标题',
                  schema=Page(title='页面上方标题', body=...., style=background_css))
#添加页面到admin_app
admin_app.pages[0].children.append(xxx_page)
```


## 丨❤鸣谢
- 来自[LittlePaimon](https://github.com/CMHopeSunshine/LittlePaimon)的webui代码参考
- 来自[nonebot-plugin-updater](https://github.com/hanasa2023/nonebot-plugin-updater#readme)的nb安装代码
