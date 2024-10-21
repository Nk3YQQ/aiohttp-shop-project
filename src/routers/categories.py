import json

import aiohttp.web as web
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError

from src.database import async_session
from src.models import Category
from src.schemas import CategoryCreate, Category as CategorySchema
from src.session import create, read_all, read_one, update_obj, delete_obj

routes = web.RouteTableDef()


async def read_category(session, model, instance_id):
    category = await read_one(session, model, instance_id)

    if not category:
        msg = {'detail': 'категория не найдена'}
        raise web.HTTPNotFound(body=json.dumps(msg, ensure_ascii=False))

    return category


@routes.post('/')
async def add_product(request: web.Request):
    try:
        data = await request.json()

        category = CategoryCreate(**data)

        category_item = Category(title=category.title)

        await create(async_session, category_item)

        return web.json_response(CategorySchema.from_orm(category_item).dict(), status=201)

    except IntegrityError:
        return web.json_response({'detail': 'категория уже создана'}, status=400)

    except ValidationError as e:
        msg = {
            'error': 'неверный формат данных для категории',
            'detail': e.errors()
        }
        return web.json_response(msg, status=400)


@routes.get('/')
async def get_categories(request: web.Request):
    skip = request.query.get('skip', 0)
    limit = request.query.get('limit', 10)

    categories = await read_all(async_session, Category, skip, limit)

    return web.json_response(list(CategorySchema.from_orm(category).dict() for category in categories))


@routes.get('/{instance_id}')
async def get_category(request: web.Request):
    try:
        instance_id = int(request.match_info.get('instance_id'))

        category = await read_category(async_session, Category, instance_id)

        return web.json_response(CategorySchema.from_orm(category).dict())

    except ValueError:
        return web.json_response({'detail': 'неправильный формат для id'}, status=400)


@routes.put('/{instance_id}')
async def update_category(request: web.Request):
    try:
        data = await request.json()
        category = CategoryCreate(**data)
        instance_id = int(request.match_info.get('instance_id'))

        await read_category(async_session, Category, instance_id)

        await update_obj(async_session, Category, instance_id, category.dict())

        return web.json_response({'detail': 'запись обновлена'})

    except IntegrityError:
        return web.json_response({'detail': 'категория уже создана'}, status=400)

    except ValidationError as e:
        msg = {
            'error': 'неверный формат данных для категории',
            'detail': e.errors()
        }
        return web.json_response(msg, status=400)

    except ValueError:
        return web.json_response({'detail': 'неправильный формат для id'}, status=400)


@routes.delete('/{instance_id}')
async def delete_category(request: web.Request):
    try:
        instance_id = int(request.match_info.get('instance_id'))

        await read_category(async_session, Category, instance_id)

        await delete_obj(async_session, Category, instance_id)

        return web.json_response(status=204)

    except ValueError:
        return web.json_response({'detail': 'неправильный формат для id'}, status=400)
