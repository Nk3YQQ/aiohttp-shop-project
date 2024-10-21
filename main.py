import aiohttp.web as web
from src.routers.categories import routes as category_routes

if __name__ == '__main__':
    app = web.Application()

    category_app = web.Application()
    category_app.add_routes(category_routes)
    app.add_subapp('/categories', category_app)

    web.run_app(app, port=8080)
