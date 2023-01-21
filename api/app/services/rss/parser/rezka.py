from datetime import datetime, date, time, timezone, timedelta

from app.serializers.feed import Item
from ._parser import WebParser

from pprint import pprint


_constant_datetime = datetime.combine(
    date(year=2023, month=1, day=21), time(
        hour=8), timezone(offset=timedelta(hours=0))
)

# NOTE: deprecated by hdrezka.me


class RezkaFeed(WebParser):
    @property
    async def items(self):
        show_url = self.feed.url
        return [
            Item(
                title=self._show_status,
                link=show_url,
                text=self._show_status,
                date=_constant_datetime,
            )
        ]

    @property
    def _show_status(self) -> str:
        pprint(self.soup.find_all('div'))
        return self.soup.find_all("h2")[-1].text
