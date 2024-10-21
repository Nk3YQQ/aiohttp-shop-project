import aiohttp.web as web
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError

from src.database import async_session
from src.models import Product
from src.schemas import Product as ProductSchema, ProductCreate
from src.session import create

routes = web.RouteTableDef()


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

        print(product_item)

        await create(async_session, product_item)

        new_product = ProductSchema().from_orm(product_item).dict()

        print(new_product)

        return web.json_response(new_product, status=201)

    except IntegrityError:
        return web.json_response({'detail': 'продукт уже создана'}, status=400)

    except ValidationError as e:
        msg = {
            'error': 'неверный формат данных для продукта',
            'detail': e.errors()
        }
        return web.json_response(msg, status=400)
