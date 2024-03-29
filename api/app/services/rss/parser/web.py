import logging

from rss_parser import Parser
from rss_parser.models import FeedItem

from app.utils.item_converter import convert_item
from app.serializers.feed import Item
from ._parser import WebParser
from ..exceptions import UnavailableFeed


class WebFeed(WebParser):
    @property
    async def items(self) -> list[Item]:
        try:
            return await self._get_items_from_web(self.feed.url)
        except (UnavailableFeed, ValueError):
            logging.warning("Failed to parse: " + self.feed.url)
            return []

    async def _get_items_from_web(self, url: str) -> list[Item]:
        return [
            convert_item(item)
            for item in await self.__get_feed_from_url(url)
        ]

    async def __get_feed_from_url(self, url: str) -> list[FeedItem]:
        try:
            html = await self.get_html(url)
            return Parser(html).parse().feed
        except AttributeError:
            raise ValueError
