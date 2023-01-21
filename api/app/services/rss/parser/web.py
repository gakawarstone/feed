import requests
import logging

from requests.exceptions import ConnectionError
from rss_parser import Parser
from rss_parser.models import FeedItem

from app.utils.item_converter import convert_item
from app.serializers.feed import Item
from ._base import BaseFeed as _BaseFeed


class WebFeed(_BaseFeed):
    @property
    async def items(self) -> list[Item]:
        try:
            return await self._get_items_from_web(self.feed.url)
        except ConnectionError:  # FIXME: own exception
            logging.exception("failed to parse " + self.feed.url)
            return []

    async def _get_items_from_web(self, url: str) -> list[Item]:
        return [
            convert_item(item)
            for item in await self.__get_feed_from_url(url)
        ]

    async def __get_feed_from_url(self, url: str) -> list[FeedItem]:
        logging.warning('making request to ' + url)
        xml = requests.get(url).content
        return Parser(xml).parse().feed
