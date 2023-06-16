from fastapi import FastAPI
from tortoise import Tortoise

from app.settings import DB_URL, MODELS
from app import routes, models, middlewares
from app.services.rss.supervisor import FeedsSupervisor


TASKS_ON_STARTUP = [
    models.setup(DB_URL, MODELS),
    FeedsSupervisor.on_startup(),
]


async def _on_startup():
    for task in TASKS_ON_STARTUP:
        await task


async def _on_shutdown():
    await Tortoise.close_connections()


def get_app():
    app = FastAPI()
    app.add_event_handler('startup', _on_startup)
    app.add_event_handler('shutdown', _on_shutdown)
    middlewares.setup(app)
    routes.setup(app)
    return app
