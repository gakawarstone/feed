import asyncio

from app.serializers.feed import Feed
from app.services.repositories.feed import FeedRepository
from app.services.repositories.item import ItemsRepository
from app.parsers import FeedParser


class FeedsSupervisor:
    @classmethod
    def on_startup(cls):
        asyncio.create_task(cls.__dispatcher())

    @classmethod
    async def dispatcher(cls):
        try:
            while True:
                print('fetch all feeds')
                await cls.__fetch_all_feeds()
                await asyncio.sleep(60)
        except Exception as e:
            print('DISPATCHER FAILED WITH ', e)
            import traceback
            traceback.print_exc()
            await cls.__dispatcher()

    @classmethod
    async def __fetch_all_feeds(cls):
        feeds = await FeedRepository.get_all()

        async with asyncio.TaskGroup() as tg:
            for feed in feeds:
                tg.create_task(cls.__fetch_feed(feed))

    @classmethod
    async def __fetch_feed(cls, feed: Feed):
        items = await FeedParser(feed).parse()
        await ItemsRepository(feed).add_items_to_feed(items)
