import logging

from aiohttp import web

from pet_feeding import models
from pet_feeding.tools import request_errors_middleware
LOG = logging.getLogger(__name__)


async def ping(request):
    return web.json_response({'text': 'pong'})


async def on_startup(app):
    await models.main()
    LOG.info('App is starting ...')


async def on_shutdown(app):
    LOG.info('App is stopping ...')


def setup_routes(app):
    app.router.add_get('/api/ping', ping, allow_head=False)


def create_app():
    app = web.Application(middlewares=[request_errors_middleware, ])
    setup_routes(app)
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)
    return app


if __name__ == '__main__':
    app = create_app()
    web.run_app(app, port=80)
