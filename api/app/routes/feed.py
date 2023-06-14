from asyncio import TaskGroup

from fastapi import Response, Request

from app.services.rss.generator.rss_feed_generator import FeedGenerator
from app.services.repositories.feed import FeedRepository
from app.services.rss.parser import FeedParser


async def get_rss_feed(request: Request):
    feeds = await FeedRepository.get_all()

    tasks = []
    async with TaskGroup() as tg:
        for feed in feeds:
            tasks.append(tg.create_task(FeedParser(feed).parse()))

    items = []
    for t in tasks:
        items += t.result()

    content = FeedGenerator.create_rss_feed(items)
    return Response(content=content, media_type="application/xml")
