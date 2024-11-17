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

使用webui安装、更新、卸载插件和修改`.evn.*`文件，并提供webui接入支持

## 💿 安装

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