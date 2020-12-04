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


async def create_org(request):
    data = await request.json()
    async with models.conn():
        org = await models.Organization.create(**data)
    return web.json_response({'id': org.id}, status=201)


async def get_org(request):
    _id = request.match_info['org_id']
    async with models.conn():
        org = await models.Organization.get(int(_id))
    return web.json_response(org.to_dict(), status=200)


async def create_org_user(request):
    data = await request.json()
    async with models.conn():
        user = await models.OrgUser.create(**data, organization_id=int(request.match_info['org_id']))
    return web.json_response({'id': user.id}, status=201)


async def get_user(request):
    _id = request.match_info['user_id']
    async with models.conn():
        user = await models.OrgUser.get(int(_id))
    return web.json_response(user.to_dict(), status=200)


async def add_pet(request):
    data = await request.json()
    async with models.conn():
        pet = await models.Pet.create(**data, organization_id=int(request.match_info['org_id']))
    return web.json_response({'id': pet.id}, status=201)


async def get_pet(request):
    _id = request.match_info['pet_id']
    async with models.conn():
        pet = await models.Pet.get(int(_id))
    return web.json_response(pet.to_dict(), status=200)


async def get_org_pets(request):
    _id = request.match_info['org_id']
    async with models.conn():
        pets = await models.Pet.query.where(models.Pet.org == int(_id)).gino.all()
    return web.json_response(data=[pet.to_dict() for pet in pets], status=200)


def setup_routes(app):
    app.router.add_get('/api/ping', ping, allow_head=False)
    app.router.add_post('/api/organizations', create_org)
    app.router.add_get('/api/organizations/{org_id}', get_org)
    app.router.add_get('/api/organizations/{org_id}/users/{user_id}', get_user)
    app.router.add_post('/api/organizations/{org_id}/users', create_org_user)
    app.router.add_post('/api/organizations/{org_id}/pets', add_pet)
    app.router.add_get('/api/organizations/{org_id}/pets', get_org_pets)
    app.router.add_get('/api/organizations/{org_id}/pets/{pet_id}', get_pet)


def create_app():
    app = web.Application(middlewares=[request_errors_middleware,])
    setup_routes(app)
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)
    return app


if __name__ == '__main__':
    app = create_app()
    web.run_app(app, port=81)
