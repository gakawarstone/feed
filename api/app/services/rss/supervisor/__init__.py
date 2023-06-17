import asyncio

from app.serializers.feed import Feed
from app.services.repositories.feed import FeedRepository
from app.services.repositories.item import ItemsRepository
from app.services.rss.parser import FeedParser


class FeedsSupervisor:
    @classmethod
    async def on_startup(cls):
        asyncio.create_task(cls.__dispatcher())

    @classmethod
    async def __dispatcher(cls):
        try:
            while True:
                await cls.__fetch_all_feeds()
                await asyncio.sleep(60)
        except Exception as e:
            print('DISPATCHER FAILED WITH ', e)
            await cls.__dispatcher()

    @classmethod
    async def __fetch_all_feeds(cls):
        feeds = await FeedRepository.get_all()

        tasks = []
        async with asyncio.TaskGroup() as tg:
            for feed in feeds:
                tasks.append(tg.create_task(cls.__fetch_feed(feed)))

    @classmethod
    async def __fetch_feed(cls, feed: Feed):
        items = await FeedParser(feed).parse()
        await ItemsRepository(feed).add_items_to_feed(items)
