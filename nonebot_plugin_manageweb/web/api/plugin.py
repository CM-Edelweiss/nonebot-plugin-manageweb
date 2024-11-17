import subprocess
from shutil import which
from ...logger import logger
from fastapi import APIRouter
from ...utils import authentication
from ...plugins.utils import get_plugin
from fastapi.responses import JSONResponse


route = APIRouter()


@route.get(
    '/plugins', response_class=JSONResponse, dependencies=[authentication()]
)
async def plugins():
    """获取插件列表api"""
    plugins = await get_plugin()
    return {
        'status': 0,
        'msg': 'ok',
        'data': {
            'rows': plugins,
            'total': len(plugins)
        }
    }


@route.post(
    '/plugins/install', response_class=JSONResponse, dependencies=[authentication()]
)
async def install(project_link: str):
    logger.info('MW管理器', f'开始安装插件{project_link}')
    try:
        nb = which('nb')
        if nb and project_link:
            subprocess.run(
                [nb, 'plugin', 'install', project_link], check=True
            )
            return {'status': 0, 'msg': f'{project_link}安装成功'}
    except Exception as e:
        return {'status': -100, 'msg': f'{project_link}安装失败,请查看命令行->{e}'}


@route.post(
    '/plugins/update', response_class=JSONResponse, dependencies=[authentication()]
)
async def update(project_link: str):
    logger.info('MW管理器', f'开始更新插件{project_link}')
    try:
        nb = which('nb')
        if nb and project_link:
            subprocess.run(
                [nb, 'plugin', 'update', project_link], check=True
            )
            return {'status': 0, 'msg': f'{project_link}更新成功'}
    except Exception as e:
        return {'status': -100, 'msg': f'{project_link}更新失败,请查看命令行->{e}'}


@route.post(
    '/plugins/uninstall', response_class=JSONResponse, dependencies=[authentication()]
)
async def uninstall(project_link: str):
    logger.info('MW管理器', f'开始卸载插件{project_link}')
    try:
        nb = which('nb')
        if nb:
            process = subprocess.Popen(
                [nb, 'plugin', 'uninstall', project_link],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            process.communicate(input=b'y\n')
            return {'status': 0, 'msg': f'{project_link}卸载成功'}
    except Exception as e:
        return {'status': -100, 'msg': f'{project_link}卸载失败,请查看命令行->{e}'}
