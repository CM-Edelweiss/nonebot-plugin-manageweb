from amis import (
    Page,
    PageSchema,
    Flex,
    ActionType,
    LevelEnum,
    ButtonGroupSelect,
    Log,
    Alert,
    Form,
    Dialog,
    Select,
    Group,
    InputText,
    DisplayModeEnum,
    Horizontal,
)
from ...config import config
from ...utils import logo, background_css

select_log_num = Select(
    label='日志数量',
    name='log_num',
    value=100,
    options=[
        {'label': 100, 'value': 100},
        {'label': 200, 'value': 200},
        {'label': 300, 'value': 300},
        {'label': 400, 'value': 400},
        {'label': 500, 'value': 500},
    ],
)

select_log_level = ButtonGroupSelect(
    label='日志等级',
    name='log_level',
    btnLevel=LevelEnum.light,
    btnActiveLevel=LevelEnum.info,
    value='info',
    options=[{'label': 'INFO', 'value': 'info'},
             {'label': 'DEBUG', 'value': 'debug'}],
)

log_page = Log(
    autoScroll=True,
    placeholder='暂无日志数据...',
    operation=['stop', 'showLineNumber', 'filter'],
    source={
        'method': 'get',
        'url': '/mw/api/log?level=${log_level | raw}&num=${log_num | raw}',
        'headers': {'token': config.mw_key[:16]},
    },
)

cmd_input = Form(
    mode=DisplayModeEnum.horizontal,
    horizontal=Horizontal(left=3),
    wrapWithPanel=False,
    body=[
        InputText(
            name='command',
            required=True,
            clearable=True,
            addOn=ActionType.Dialog(
                label='执行',
                level=LevelEnum.primary,
                dialog=Dialog(
                    title='命令执行结果',
                    size='xl',
                    body=Log(
                        autoScroll=True,
                        placeholder='执行命令中，请稍候...',
                        operation=['stop', 'showLineNumber', 'filter'],
                        source={
                            'method': 'get',
                            'url': '/mw/api/run_cmd?cmd=${command | raw}',
                            'headers': {'token': config.mw_key[:16]},
                        },
                    ),
                ),
            ),
        )
    ],
)

operation_button = Flex(
    justify='center',
    items=[
        ActionType.Ajax(
            label='关闭',
            className='m-l',
            api='/mw/api/bot_stop',
            confirmText='该操作将会使Bot关闭，将导致程序无法运行，请谨慎操作',
            level=LevelEnum.danger,
        ),
        ActionType.Ajax(
            label='重启',
            className='m-l',
            api='/mw/api/bot_restart',
            confirmText='该操作将会使Bot重启，在完成重启之前，该页面也将无法访问（也可能会弹出报错，可无视），请耐心等待重启',
            level=LevelEnum.danger,
        ),
        ActionType.Dialog(
            label='日志',
            className='m-l',
            level=LevelEnum.primary,
            dialog=Dialog(
                title='查看日志',
                size='xl',
                actions=[],
                body=[
                    Alert(
                        level=LevelEnum.info,
                        body='查看最近最多500条日志，不会自动刷新，需要手动点击两次"暂停键"来进行刷新，DEBUG日志需要Nonebot日志模式为DEBUG才能查看。',
                    ),
                    Form(
                        body=[
                            Group(body=[select_log_num, select_log_level]), log_page]
                    ),
                ],
            ),
        ),
        ActionType.Dialog(
            label='执行命令',
            className='m-l',
            level=LevelEnum.warning,
            dialog=Dialog(title='执行命令', size='lg',
                          actions=[], body=[cmd_input]),
        ),
    ],
)


page_detail = Page(
    title='', body=[logo, operation_button], style=background_css) # type: ignore
page = PageSchema(
    url='/home', label='首页', icon='fa fa-home', isDefaultPage=True, schema=page_detail # type: ignore
)
