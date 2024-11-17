from amis import App, Tpl, Flex
from .env import page as env_page
from .home import page as home_page
from .plugin import page as plugin_page


github_logo = Tpl(
    className='w-full',
    tpl='<div class="flex justify-between"><div></div><div><a href="https://github.com/CM-Edelweiss/nonebot-plugin-manageweb" target="_blank" title="Copyright"><i class="fa fa-github fa-2x"></i></a></div></div>',
)
header = Flex(
    className='w-full', justify='flex-end', alignItems='flex-end', items=[github_logo]
)


admin_app = App(
    brandName='MW管理器',
    logo='https://img.picui.cn/free/2024/10/28/671f78556a9ee.png',
    pages=[
        {
            'children': [
                home_page,
                plugin_page,
                env_page
            ]
        }
    ],
    header=header
)
