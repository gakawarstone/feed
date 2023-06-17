import asyncio

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

    @staticmethod
    async def __fetch_all_feeds():
        feeds = await FeedRepository.get_all()

        tasks = []
        async with asyncio.TaskGroup() as tg:
            for feed in feeds:
                tasks.append(tg.create_task(FeedParser(feed).parse()))

        for n, task in enumerate(tasks):
            await ItemsRepository(feeds[n]).add_items_to_feed(task.result())
