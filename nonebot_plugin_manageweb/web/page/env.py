from amis import (
    Action,
    Form,
    LevelEnum,
    Page,
    PageSchema,
    Editor,
    Select,

)
from ...utils import background_css

nonebot_form = Form(
    title='',
    initApi='get:/mw/api/env_config?file_name=${file_name}',
    api='post:/mw/api/env_config?file_name=${file_name}',
    body=[
        Select(
            name='file_name',
            label='选择文件',
            value='.env.prod',
            options=[
                {
                    'label': '.env',
                    'value': '.env'
                },
                {
                    'label': '.env.prod',
                    'value': '.env.prod'
                },
                {
                    'label': '.env.dev',
                    'value': '.env.dev'
                }
            ]
        ),
        Editor(
            name='editor',
            label='编辑',
            value='${data}',
            placeholder='暂无内容'
        )
    ],
    actions=[Action(label='保存', level=LevelEnum.success, type='submit')]
)

page = PageSchema(url='/configs', icon='fa fa-wrench', label='Nonebot配置',
                  schema=Page(title='Nonebot配置', body=nonebot_form, style=background_css))  # type: ignore
