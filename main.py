import aiohttp.web as web
from src.routers.categories import routes as category_routes
from src.routers.products import routes as product_routes

if __name__ == '__main__':
    app = web.Application()

    category_app = web.Application()
    category_app.add_routes(category_routes)
    app.add_subapp('/categories', category_app)

    product_app = web.Application()
    product_app.add_routes(product_routes)
    app.add_subapp('/products', product_app)

    web.run_app(app, port=8080)
