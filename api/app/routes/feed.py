from fastapi import Response, Request

from app.services.rss.generator.rss_feed_generator import FeedGenerator
from app.services.repositories.feed import FeedRepository
from app.services.rss.parser import FeedParser


async def get_rss_feed(request: Request):
    feeds = await FeedRepository.get_all()

    items = []
    for feed in feeds:
        items += await FeedParser(feed).parse()

    content = FeedGenerator.create_rss_feed(items)
    return Response(content=content, media_type="application/xml")
