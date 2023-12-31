import asyncio
from asyncpg.pool import Pool
import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
from tortoise.contrib.fastapi import register_tortoise
from bot.database.db_requests import get_catalog
from bot.config import Config, load_config
from bot.main import create_pool


def create_app(connector: Pool):
    app = FastAPI(debug=True)

    templates = Jinja2Templates(directory="templates")

    @app.get("/", response_class=HTMLResponse)
    async def read_root(request: Request):
        async with connector.acquire() as connect:
            catalog = await get_catalog()
            return templates.TemplateResponse("item.html", {"request": request, "catalog": catalog})

    return app


def start_uvicorn(loop):
    config: Config = load_config('.env.app')
    connector: Pool = loop.run_until_complete(create_pool(config))
    db_request: DBRequest = DBRequest()
    app = create_app(db_request, connector)
    register_tortoise(
        app,
        db_url=config.db_url(),
        modules={"models": ["database.models", "aerich.models"]},
        generate_schemas=True,
        add_exception_handlers=True,
    )
    config = uvicorn.Config(app, loop=loop)
    server = uvicorn.Server(config)
    loop.run_until_complete(server.serve())


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    start_uvicorn(loop)

