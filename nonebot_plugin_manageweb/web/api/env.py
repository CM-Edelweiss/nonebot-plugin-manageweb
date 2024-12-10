from pathlib import Path
from ...logger import logger
from fastapi import APIRouter
from ...utils import authentication
from fastapi.responses import JSONResponse


route = APIRouter()


@route.get('/env_config', response_class=JSONResponse, dependencies=[authentication()])
async def env_config(file_name: str):
    try:
        return {
            'status': 0,
            'msg':    'ok',
            'data':   {
                'data': (Path() / file_name).read_text(encoding='utf-8')
            }
        }
    except Exception as e:
        logger.info('MW管理器', f'获取{file_name}文件失败: {e}')
        return {
            'status': -100,
            'msg':    f'获取文件失败->{e}',
        }


@route.post('/env_config', response_class=JSONResponse, dependencies=[authentication()])
async def env_config_w(file_name: str, data: dict):
    try:
        with open(Path() / file_name, 'w', encoding='utf-8') as f:
            f.write(data['editor'])
        return {
            'status': 0,
            'msg':    f'{file_name}文件保存成功'
        }
    except Exception as e:
        logger.info('MW管理器', f'保存{file_name}文件失败: {e}')
        return {
            'status': -100,
            'msg':    f'保存文件失败->{e}',
        }
