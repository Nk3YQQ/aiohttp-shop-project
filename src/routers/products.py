import json

import aiohttp.web as web
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError

from src.database import async_session
from src.models import Product
from src.schemas import Product as ProductSchema, ProductCreate
from src.session import create, read_all, read_one, update_obj, delete_obj

routes = web.RouteTableDef()


async def read_product(session, model, instance_id):
    product = await read_one(session, model, instance_id)

    if not product:
        msg = {'detail': 'категория не найдена'}
        raise web.HTTPNotFound(body=json.dumps(msg, ensure_ascii=False))

    return product


@routes.post('/')
async def add_product(request: web.Request):
    try:
        data = await request.json()

        product = ProductCreate(**data)

        product_item = Product(
            title=product.title,
            description=product.description,
            price=product.price,
            category_id=product.category_id
        )

        await create(async_session, product_item)

        return web.json_response({'detail': 'продукт создан'}, status=201)

    except IntegrityError:
        return web.json_response({'detail': 'продукт уже создана'}, status=400)


@routes.get('/')
async def get_products(request: web.Request):
    skip = request.query.get('skip', 0)
    limit = request.query.get('limit', 10)

    products = await read_all(async_session, Product, skip, limit, mode='products')

    return web.json_response(list(ProductSchema.from_orm(product).dict() for product in products))


@routes.get('/{instance_id}')
async def get_product(request: web.Request):
    try:
        instance_id = int(request.match_info.get('instance_id'))

        product = await read_product(async_session, Product, instance_id)

        return web.json_response(ProductSchema.from_orm(product).dict())

    except ValueError:
        return web.json_response({'detail': 'неправильный формат для id'}, status=400)


@routes.put('/{instance_id}')
async def update_product(request: web.Request):
    try:
        data = await request.json()
        product = ProductCreate(**data)
        instance_id = int(request.match_info.get('instance_id'))

        await read_product(async_session, Product, instance_id)

        await update_obj(async_session, Product, instance_id, product.dict())

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
async def delete_product(request: web.Request):
    try:
        instance_id = int(request.match_info.get('instance_id'))

        await read_product(async_session, Product, instance_id)

        await delete_obj(async_session, Product, instance_id)

        return web.json_response(status=204)

    except ValueError:
        return web.json_response({'detail': 'неправильный формат для id'}, status=400)
