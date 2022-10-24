from rss_parser import Parser
import requests
from datetime import datetime

from item import Item


def parse_feed(url: str) -> list[Item]:
    xml = requests.get(url).content
    feed = Parser(xml).parse().feed
    return [
        Item(
            title=item.title,
            text=item.description,
            date=datetime.now(),
            link=item.link
        )
        for item in feed
    ]
