from datetime import datetime, timezone, timedelta
from dateutil.parser import parse
import requests

from rss_parser import Parser

from ..types import Item

# [ ] exceptions


class RssFeedParser:
    @classmethod
    def parse_from_url(cls, url: str) -> list[Item]:
        xml = requests.get(url).content
        feed = Parser(xml).parse().feed
        return [
            Item(
                title=item.title,
                text=item.description,
                date=datetime.combine(parse(item.publish_date).date(),
                                      parse(item.publish_date).time(),
                                      timezone(offset=timedelta(hours=0))),
                link=item.link
            )
            for item in feed
        ]
