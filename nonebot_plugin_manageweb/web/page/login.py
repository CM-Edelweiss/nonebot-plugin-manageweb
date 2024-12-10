from amis import (
    Page,
    Remark,
    InputPassword,
    AmisAPI,
    Wrapper,
    Horizontal,
    Form,
    DisplayModeEnum,
    InputText,
    LevelEnum,
    Action
)

from ...utils import logo, background_css, rounded_css_9

# -------------登录-------------------#


login_api = AmisAPI(
    url="/mw/api/login",
    method="post",
    adaptor="""
        if (payload.status == 0) {
            localStorage.setItem("token", payload.data.token);
        }
        return payload;
    """,
)

login_body = Wrapper(className="w-2/5 mx-auto my-0 m:w-full", body=Form(
    api=login_api,
    title="",
    body=[
        logo,
        InputText(
            name="username",
            label="用户名",
            labelRemark=Remark(
                shape="circle", content="后台管理用户名，默认为pmhelp"),
        ),
        InputPassword(
            name="password",
            label="密码",
            labelRemark=Remark(
                shape="circle", content="后台管理密码，默认为admin"),
        ),
    ],
    mode=DisplayModeEnum.horizontal,
    style=rounded_css_9, # type: ignore
    actions=[Action(label='登录', level=LevelEnum.primary, type='submit', style={ # type: ignore
        "display": "table",
        "margin": "0 auto",
        "border-radius": "2em",
    })],
    horizontal=Horizontal(left=3, right=7, offset=5),
    redirect="/mw/admin",
))

login_page = Page(title="", body=login_body, style=background_css) # type: ignore
