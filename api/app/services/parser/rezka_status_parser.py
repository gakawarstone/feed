import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, timezone, date, time

from ..types import Item
from .rss_feed_parser import RssFeedParser

_headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        "AppleWebKit/537.36 (KHTML, like Gecko)"
        "Chrome/106.0.0.0 Safari/537.36"
    )
}

_constant_datetime = datetime.combine(
    date(year=2022, month=11, day=28), time(
        hour=8), timezone(offset=timedelta(hours=0))
)


class RezkaShowFeedParser(RssFeedParser):
    @classmethod
    def parse_show(cls, show_url: str) -> list[Item]:
        print('parsing show: ' + show_url)
        return [
            Item(
                title=cls.get_rezka_show_status(show_url),
                link=show_url,
                text=cls.get_rezka_show_status(show_url),
                date=_constant_datetime,
            )
        ]

    @classmethod
    def get_rezka_show_status(cls, url: str) -> str:
        html = requests.get(url, headers=_headers)
        soup = BeautifulSoup(html.content, "html.parser")

        return soup.find_all("h2")[-1].text
