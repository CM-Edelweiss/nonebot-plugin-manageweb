import datetime
from jose import jwt
from .logger import logger
from fastapi import FastAPI
from pydantic import BaseModel
from .web.api import BaseApiRouter
from nonebot import get_app, get_driver
from nonebot.plugin import PluginMetadata
from .web.page import admin_app, login_page
from .config import Config, config as mw_config
from .utils import requestAdaptor, responseAdaptor
from fastapi.responses import JSONResponse, HTMLResponse, RedirectResponse

DRIVER = get_driver()


__plugin_meta__ = PluginMetadata(
    name='nb商店插件安装器web版',
    description='Nonebot插件商店安装插件，使用基于fastapi和amis的webui安装',
    type="application",
    usage="webui服务",
    homepage="https://github.com/CM-Edelweiss/nonebot-plugin-manageweb",
    config=Config,
    supported_adapters=None,
    extra={
        'author': 'CM-Edelweiss',
        'version': '0.1.0',
        'priority': 1,
    },
)


class UserModel(BaseModel):
    username: str
    password: str


@DRIVER.on_startup
async def init_web():
    """主程序"""
    try:
        app: FastAPI = get_app()
        app.include_router(BaseApiRouter)
        logger.info(
            "MW webui",
            f"<g>启用成功</g>，默认地址为<m>http://{DRIVER.config.host}:{DRIVER.config.port}/mw/login</m>",
        )
    except Exception as e:
        return logger.info('MW webui', f'启用<r>失败：{e}</r>')

    @app.post("/mw/api/login", response_class=JSONResponse)
    async def login(user: UserModel):
        """登录api"""
        if (
            user.username != mw_config.mw_username
            or user.password != mw_config.mw_password
        ):
            return {"status": -100, "msg": "登录失败，请确认用户ID和密码无误"}
        token = jwt.encode(
            {
                "username": user.username,
                "exp": datetime.datetime.now(datetime.timezone.utc)
                + datetime.timedelta(minutes=30),
            },
            mw_config.mw_key,
            algorithm="HS256",
        )
        return {"status": 0, "msg": "登录成功", "data": {"token": token}}

    @app.get("/mw", response_class=RedirectResponse)
    async def redirect_page():
        return RedirectResponse("/mw/login")

    @app.get("/mw/login", response_class=HTMLResponse)
    async def login_page_app():
        return login_page.render(
            site_title="登录 | MW 后台管理",
            site_icon="https://img.picui.cn/free/2024/10/28/671f78556a9ee.png",
            theme="ang"
        )

    @app.get("/mw/admin", response_class=HTMLResponse)
    async def admin_page_app():
        return admin_app.render(
            site_title="MW 后台管理",
            site_icon="https://img.picui.cn/free/2024/10/28/671f78556a9ee.png",
            theme="ang",
            requestAdaptor=requestAdaptor,
            responseAdaptor=responseAdaptor,
        )
