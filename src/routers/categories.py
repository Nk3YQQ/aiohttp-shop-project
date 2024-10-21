import aiohttp.web as web

from src.database import async_session
from src.models import Category
from src.session import create

routes = web.RouteTableDef()


@routes.post('/')
async def add_product(request: web.Request):
    data = await request.json()

    category = Category(**data)

    await create(async_session, category)

    return web.json_response({'detail': 'категория создана'})
