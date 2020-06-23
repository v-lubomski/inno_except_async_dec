from aiohttp import web
import aiosqlite
import asyncio
from jsonschema import validate
from exceptions.exceptions_for_exc2 import ValidationError

SCHEMA = ''


async def create_connection():
    return await aiosqlite.connect('deliveries.sqlite')


async def init_app():
    app = web.Application()
    app["engine"] = await create_connection()
    await create_db(app["engine"])
    app.add_routes(routes)
    return app


async def create_db(db):
    await db.execute(
        'CREATE TABLE IF NOT EXISTS statuses('
        'identifier VARCHAR(5) NOT NULL PRIMARY KEY,'
        'status VARCHAR(20) NOT NULL);')
    await db.commit()


async def read_from_db(db):
    output = ''
    async with db.execute('SELECT * FROM statuses') as cursor:
        async for row in cursor:
            output += str(row) + '\n'
    return output


async def write_to_db(db, identifier, status):
    await db.execute(
        'INSERT OR REPLACE INTO statuses(identifier, status) VALUES (?,?)',
        (identifier, status))
    await db.commit()


routes = web.RouteTableDef()


@routes.get('/read')
async def give_deliveries(request):
    return web.Response(text=await asyncio.shield(read_from_db(request.app['engine'])))


@routes.post('/write')
async def get_request(request):
    body = await request.json()
    try:
        validate(schema=SCHEMA, instance=body)
    except ValidationError:
        raise ValidationError
    else:
        for identifier, status in body.items():
            await asyncio.shield(write_to_db(request.app['engine'], identifier, status))
        return web.Response(text='Data successfully written')


if __name__ == '__main__':
    web.run_app(init_app())
