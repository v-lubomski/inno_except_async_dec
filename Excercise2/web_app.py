from aiohttp import web
import aiosqlite


async def init_app():
    await create_db()
    app = web.Application()
    app.add_routes(routes)
    return app


async def create_db():
    async with aiosqlite.connect('deliveries.sqlite') as db:
        await db.execute(
            'CREATE TABLE IF NOT EXISTS statuses('
            'identifier VARCHAR(5) NOT NULL PRIMARY KEY,'
            'status VARCHAR(20) NOT NULL);')
        await db.commit()


async def read_from_db():
    output = ''
    async with aiosqlite.connect('deliveries.sqlite') as db:
        async with db.execute('SELECT * FROM statuses') as cursor:
            async for row in cursor:
                output += str(row) + '\n'
    return output


async def write_to_db(identifier, status):
    async with aiosqlite.connect('deliveries.sqlite') as db:
        await db.execute(
            'INSERT OR REPLACE INTO statuses(identifier, status) VALUES (?,?)',
            (identifier, status))
        await db.commit()


routes = web.RouteTableDef()


@routes.get('/read')
async def give_deliveries(request):
    return web.Response(text=await read_from_db())


@routes.post('/write')
async def get_request(request):
    body = await request.json()
    for identifier, status in body.items():
        await write_to_db(identifier, status)
    return web.Response(text='Data successfully written')


if __name__ == '__main__':
    web.run_app(init_app())
