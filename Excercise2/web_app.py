from aiohttp import web
import aiosqlite
import asyncio
from json import load
from jsonschema import validate, ValidationError

with open('schema.json', encoding='utf-8') as file:
    SCHEMA = load(file)


async def init_app():
    app = web.Application()
    app["engine"] = await aiosqlite.connect('deliveries.sqlite')
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


async def write_to_db(db, json_data):
    await db.execute(
        'INSERT OR REPLACE INTO statuses(identifier, status) VALUES (?,?)',
        (json_data['identifier'], json_data["status"]))
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
    except ValidationError as ex:
        return web.Response(text=f"Валидация не пройдена\n\n{ex}", status=400)
    else:
        await asyncio.shield(write_to_db(request.app['engine'], body))
        return web.Response(text='Data successfully written')


if __name__ == '__main__':
    web.run_app(init_app())
