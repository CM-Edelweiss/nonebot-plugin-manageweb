import asyncio
import inspect
from shutil import which
from pathlib import Path
from ...config import config
from typing import Union, Optional
from ...utils import authentication
from fastapi import APIRouter, Header
from fastapi.responses import JSONResponse, StreamingResponse
from nonebot.log import logger, default_filter, default_format


route = APIRouter()


info_logs = []
debug_logs = []


def record_info_log(message: str):
    info_logs.append(message)
    if len(info_logs) > 500:
        info_logs.pop(0)


def record_debug_log(message: str):
    # 过滤一些无用日志
    if not any(w in message for w in {'Checking for matchers', 'Running PreProcessors', 'OneBot V11 | Calling API'}):
        debug_logs.append(message)
        if len(debug_logs) > 300:
            debug_logs.pop(0)


logger.add(record_info_log, level='INFO', colorize=True,
           filter=default_filter, format=default_format)
logger.add(record_debug_log, level='DEBUG', colorize=True,
           filter=default_filter, format=default_format)


@route.post(
    '/bot_stop', response_class=JSONResponse, dependencies=[authentication()]
)
async def stop() -> None:
    from uvicorn.server import Server
    fis = inspect.getouterframes(inspect.currentframe())
    svrs = (fi.frame.f_locals.get('server', None) for fi in fis[::-1])
    server, *_ = (s for s in svrs if isinstance(s, Server))
    server.should_exit = True


@route.post(
    '/bot_restart', response_class=JSONResponse, dependencies=[authentication()]
)
async def restart() -> None:
    from os import execlp

    nb = which('nb')
    py = which('python')
    if nb:
        execlp(nb, nb, 'run')
    elif py:
        from sys import argv

        if argv and Path(argv[0]).exists():
            execlp(py, py, argv[0])
        if Path('bot.py').exists():
            execlp(py, py, 'bot.py')
    raise Exception('无法重启')


@route.get('/log')
async def get_log(token: Optional[str] = Header(...), level: str = 'info', num: Union[int, str] = 100):
    if token != config.mw_key[:16]:
        return '非法请求'
    show_logs = info_logs[-int(num or 1)
                               :] if level == 'info' else debug_logs[-int(num or 1):]

    async def streaming_logs():
        for log in show_logs:
            yield log
            await asyncio.sleep(0.02)

    return StreamingResponse(streaming_logs())


@route.get('/run_cmd')
async def run_cmd(token: Optional[str] = Header(...), cmd: str = ''):
    if token != config.mw_key[:16]:
        return '非法请求'
    if not cmd:
        return '无效命令'
    p = await asyncio.create_subprocess_shell(cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    return StreamingResponse(p.stdout or p.stderr) # type: ignore
