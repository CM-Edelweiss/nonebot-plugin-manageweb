from pydantic import BaseModel
from nonebot import get_plugin_config


class Config(BaseModel):
    # 后台管理用户名
    mw_username: str = "admin"
    # 后台管理密码
    mw_password: str = "admin"
    # 后台管理token密钥
    mw_key: str = "r99nxsvr93a5da907dy7adi241mvisjydxspiwxgpiyoh9nas35036fkxd7y"


config: Config = get_plugin_config(Config)
