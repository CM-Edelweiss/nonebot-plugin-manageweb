import toml
import httpx
from typing import Any
from pathlib import Path
import importlib_metadata
from .models import NBPluginMetadata


async def get_store_plugins() -> list[NBPluginMetadata]:
    """获取nb商店中的所有插件

    Returns:
        list[NBPluginMetadata]: 插件元信息列表
    """
    async with httpx.AsyncClient() as ctx:
        response: httpx.Response = await ctx.get(
            'https://registry.nonebot.dev/plugins.json'
        )
        if response.status_code == 200:
            data: list[NBPluginMetadata] = [
                NBPluginMetadata(**item) for item in response.json()
            ]
            return data
    raise httpx.NetworkError('获取nb商店插件信息失败')


def find_project_root() -> Path:
    """获取项目根目录

    Raises:
        FileNotFoundError: 无法找到项目根目录

    Returns:
        Path: 项目根目录
    """
    parent: Path = Path.cwd().resolve()
    if (parent / 'pyproject.toml').exists():
        return parent
    raise FileNotFoundError(
        "Could not find 'pyproject.toml' in any parent directory")


def get_plugin_module_list() -> list[str]:
    """从项目根目录下的pyproject.toml中获取已安装的插件列表

    Returns:
        list[str]: 已安装的插件列表
    """
    project_root: Path = find_project_root()
    pyproject_path: Path = project_root / 'pyproject.toml'
    config: dict[str, Any] = toml.load(pyproject_path)
    plugin_list: list[str] = config['tool']['nonebot']['plugins']
    return plugin_list


async def get_plugin():
    """处理插件信息

    Returns:
        list[str]: 已处理的插件列表
    """
    store_plugins: list[NBPluginMetadata] = await get_store_plugins()
    plugin_module_list: list[str] = get_plugin_module_list()
    for plugin in store_plugins:
        for module in plugin_module_list:
            if module == plugin.module_name:
                plugin.is_installed = True
                plugin.current_version = importlib_metadata.version(
                    plugin.project_link.replace('-', '_'))
    return store_plugins
