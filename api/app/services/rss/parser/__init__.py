from typing import Type

from app.serializers.feed import Feed, Item
from .web import WebFeed
from .tiktok import TikTokFeed
from ._base import TFeedParser
from .kinogo import KinogoFeed


_PARSERS: dict[str, Type[TFeedParser]] = {
    'web': WebFeed,
    'tiktok': TikTokFeed,
    'kinogo': KinogoFeed,
}


class FeedParser:
    _parsers = _PARSERS

    def __init__(self, feed: Feed):
        self.feed = feed
        if self.feed.type not in _PARSERS:
            raise ValueError(f'Unknown feed type: {self.feed.type}')

    async def parse(self) -> list[Item]:
        parser = self._parsers[self.feed.type]
        return await parser(self.feed).items
