from pydantic import BaseModel


class Tag(BaseModel):
    label: str
    color: str


class NBPluginMetadata(BaseModel):
    module_name: str
    """插件模块名称"""
    project_link: str
    """插件项目包名"""
    name: str
    """插件名"""
    desc: str
    """插件描述"""
    author: str
    """插件作者"""
    homepage: str
    """插件主页"""
    tags: list[Tag]
    """插件标签"""
    is_official: bool
    """是否官方插件"""
    type: str | None
    """插件类型"""
    supported_adapters: list[str] | None
    """支持的适配器"""
    valid: bool
    """插件是否有效"""
    version: str
    """插件版本"""
    time: str
    """插件发布时间"""
    skip_test: bool
    """是否跳过测试"""

    is_installed: bool = False
    """是否已安装"""
    current_version: str | None
    """当前版本"""
