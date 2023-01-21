from fastapi.responses import JSONResponse

from app.services.repositories.feed import FeedRepository
from app.serializers.feed import Feed


async def add_feed(feed: Feed):
    await FeedRepository.create(feed)
    return JSONResponse(content={
        'created': True,
        'item': feed.dict(),
    })
