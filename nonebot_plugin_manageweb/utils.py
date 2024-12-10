from amis import Html
from .config import config
from typing import Optional
from fastapi import Header, HTTPException, Depends
from jose import jwt, JWTError, ExpiredSignatureError

requestAdaptor = """
requestAdaptor(api) {
    api.headers["token"] = localStorage.getItem("token");
    return api;
},
"""
responseAdaptor = """
responseAdaptor(api, payload, query, request, response) {
    if (response.data.detail == '登录验证失败或已失效，请重新登录') {
        window.location.href = '/mw/login'
        window.localStorage.clear()
        window.sessionStorage.clear()
        window.alert('登录验证失败或已失效，请重新登录')
    }
    return payload
},
"""

# 背景图
background_css = {
    "position": "absolute",
    "top": "0",
    "left": "0",
    "width": "100%",
    "height": "100%",
    "background": "url('https://www.loliapi.com/acg/') no-repeat center center",
    "background-size": "100% 100%",
    "backdrop-filter": "blur(10px)",
    "-webkit-backdrop-filter": "blur(10px)",
}
# 圆角/透明
rounded_css_curd = {
    "background-color": "rgba(255, 255, 255, 0.9)",
    "border-radius": "2em",
    "width": "350px",
    "transform": "translateX(5%)"
}

rounded_css_9 = {
    "background-color": "rgba(255, 255, 255, 0.9)",
    "border-radius": "2em",
}
rounded_css_8 = {
    "background-color": "rgba(255, 255, 255, 0.8)",
    "border-radius": "2em",
}

logo = Html(
    html="""
<p align="center">
    <a href="https://github.com/CM-Edelweiss/nonebot-plugin-manageweb/">
        <img src="https://img.picui.cn/free/2024/10/28/671f78556a9ee.png" width="256" height="256" alt="MW">
    </a>
</p>
<h1 align="center">Nonebot-plugin-manageweb 控制台</h1>
<div align="center">
    <a href="https://github.com/CM-Edelweiss/nonebot-plugin-manageweb" target="_blank">
        Github仓库</a>
</div>
<br>
<br>
"""
)


def authentication():
    def inner(token: Optional[str] = Header(...)):
        if token is None:
            raise HTTPException(status_code=400, detail="Token is missing")
        try:
            payload = jwt.decode(
                token, config.mw_key, algorithms="HS256"
            )
            if (
                not (username := payload.get("username"))
                or username != config.mw_username
            ):
                raise HTTPException(status_code=400, detail="登录验证失败或已失效，请重新登录")
        except (JWTError, ExpiredSignatureError, AttributeError):
            raise HTTPException(status_code=400, detail="登录验证失败或已失效，请重新登录")

    return Depends(inner)
