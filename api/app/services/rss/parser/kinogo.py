from datetime import timedelta

from app.utils.datetime import constant_datetime
from app.serializers.feed import Item
from ..exceptions import UnavailableFeed
from ._parser import WebParser


class KinogoFeed(WebParser):
    _cache_storage_time = timedelta(hours=1)

    @property
    async def items(self) -> list[Item]:
        try:
            return [
                Item(
                    title=self._show_title + ' ' + self._show_status,
                    text=self._show_status,
                    date=constant_datetime,
                    link=self.feed.url,
                )
            ]
        except (UnavailableFeed, ValueError):
            return []

    @property
    def _show_status(self) -> str:
        try:
            return self.soup.find_all(class_='status7')[0].text
        except IndexError:
            raise ValueError

    @property
    def _show_title(self) -> str:
        try:
            return self.soup.find_all('h1')[0].text
        except IndexError:
            raise ValueError('Couldn\'n find status of show: ' + self.feed.url)
