from app.utils.datetime import constant_datetime
from app.serializers.feed import Item
from ._parser import WebParser


class KinogoFeed(WebParser):
    @property
    async def items(self) -> list[Item]:
        return [
            Item(
                title=self._show_title + ' ' + self._show_status,
                text=self._show_status,
                date=constant_datetime,
                link=self.feed.url,
            )
        ]

    @property
    def _show_status(self) -> str:
        return self.soup.find_all(class_='status7')[0].text

    @property
    def _show_title(self) -> str:
        return self.soup.find_all('h1')[0].text
