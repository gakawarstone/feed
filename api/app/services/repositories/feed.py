from app.models.feed import Feed as _Feed
from app.serializers.feed import Feed


class FeedRepository:
    @classmethod
    async def create(cls, item: Feed) -> None:
        await _Feed.create(title=item.title, url=item.url, type=item.type)

    @classmethod
    async def get_all(cls) -> list[Feed]:
        return [await cls._unserialize(f) for f in (await _Feed.all())]

    @classmethod
    async def _unserialize(cls, feed: _Feed) -> Feed:
        return Feed(id=feed.id, title=feed.title, url=feed.url, type=feed.type)
