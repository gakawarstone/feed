from fastapi import FastAPI
import settings
import routes


def get_app() -> FastAPI:
    app = FastAPI()
    routes.setup(app)
    return app
