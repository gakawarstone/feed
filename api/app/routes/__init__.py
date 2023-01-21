from fastapi import FastAPI
from .add import add_feed
from .feed import get_rss_feed


def setup(app: FastAPI):
    app.add_api_route('/feed', get_rss_feed)
    app.add_api_route('/add', add_feed)
