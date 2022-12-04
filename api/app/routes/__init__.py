from fastapi import FastAPI
from .feed import show_rss


def setup(app: FastAPI):
    app.add_api_route('/feed', show_rss)
