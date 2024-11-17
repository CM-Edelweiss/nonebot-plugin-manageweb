from fastapi import APIRouter
from .env import route as env_route
from .home import route as home_route
from .plugin import route as plugin_route

BaseApiRouter = APIRouter(prefix='/mw/api')
BaseApiRouter.include_router(home_route)
BaseApiRouter.include_router(plugin_route)
BaseApiRouter.include_router(env_route)
