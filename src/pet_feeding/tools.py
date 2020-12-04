from aiohttp import web


class AmountError(Exception):
    pass


@web.middleware
async def request_errors_middleware(request, handler):
    """
    Middleware to handle common exceptions from handlers.

    For unique cases use ./tools.expects decorator.
    """
    try:
        return await handler(request)
    except Exception as e:
        return web.json_response({'message': 'Something went wrong'}, status=500)
