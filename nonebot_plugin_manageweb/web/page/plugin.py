from amis import (
    Divider,
    Card,
    Tpl,
    CRUD,
    Cards,
    Page,
    Icon,
    Status,
    DisplayModeEnum,
    InputText,
    Switch,
    LevelEnum,
    Action,
    PageSchema,
)
from ...utils import rounded_css_9, rounded_css_8, background_css, rounded_css_curd

# -------------操作-------------------#

installation_button = Action(
    label='安装',
    level=LevelEnum.success,
    style={"color": "#4CAF50", "border-radius": "2em", },  # type: ignore
    reload='cards',
    actionType="ajax",
    api="/mw/api/plugins/install?project_link=${project_link}",  # type: ignore
    confirmText="确定安装该插件吗？",
    hiddenOn='${is_installed}'
)

update_button = Action(
    label='从${current_version}更新到最新',
    style={"color": "#FFD700", "border-radius": "2em", },  # type: ignore
    reload='cards',
    actionType="ajax",
    api="/mw/api/plugins/update?project_link=${project_link}",  # type: ignore
    confirmText="确定更新该插件吗？",
    level=LevelEnum.warning,
    visibleOn='${is_installed}',
    hiddenOn='${version == current_version}'
)

uninstall_button = Action(
    label='卸载',
    style={"color": "#FF0000", "border-radius": "2em", },  # type: ignore
    reload='cards',
    actionType="ajax",
    api="/mw/api/plugins/uninstall?project_link=${project_link}", # type: ignore
    confirmText="确定卸载该插件吗？",
    level=LevelEnum.danger,
    visibleOn='${is_installed}'
)


toolbar_version = Tpl(
    tpl='V$version', className='text-secondary m-1'
)
toolbar_state = Status(value='${valid}', className="m-1")
toolbar_official = Icon(
    icon="fas fa-user",
    className="text-success m-1",
    visibleOn='${is_official}')

# -------------卡片-------------------#
card = Card(
    header=Card.Header(
        title='$name',
        subTitle='$author',
        description='$desc'
    ),
    itemAction=Action(actionType="url", confirmText="确定访问吗？",
                      url='${homepage}', blank=True),  # type: ignore
    actions=[installation_button, update_button, uninstall_button],
    style=rounded_css_curd,  # type: ignore
    className='m-l',
    toolbar=[toolbar_version, Divider(), toolbar_state, toolbar_official],
)


class CardsCRUD(CRUD, Cards):
    """卡片CRUD"""


cards_curd = CardsCRUD(
    name='cards',
    mode='cards',
    title='',
    syncLocation=False,
    api='/mw/api/plugins',
    loadDataOnce=True,
    source='${rows | filter:name:match:keywords_name | filter:author:match:keywords_author | filter:desc:match:keywords_desc | filter:is_installed:match:keywords_installed}',
    filter={
        'body': [
            InputText(name='keywords_name', label='插件名'),
            InputText(name='keywords_author', label='作者'),
            InputText(name='keywords_desc',
                      label='插件描述'),
            Switch(name='keywords_installed',
                   onText='已安装', offText='全部'),
            Action(
                label='搜索', level=LevelEnum.primary, type='submit')
        ],
        "style": rounded_css_9,
        "mode": DisplayModeEnum.inline
    },
    style=rounded_css_8,  # type: ignore
    perPage=12,
    autoJumpToTopOnPagerChange=True,
    placeholder='暂无插件信息',
    headerToolbar=['switch-per-page', 'pagination'],
    footerToolbar=[],
    card=card
)


page = PageSchema(url='/plugins', icon='fa fa-shopping-bag', label='商店',
                  schema=Page(title='商店', body=cards_curd, style=background_css))  # type: ignore
