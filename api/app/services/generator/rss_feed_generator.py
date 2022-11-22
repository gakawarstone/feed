from feedgen.feed import FeedGenerator as _FeedGenerator

from settings import SOURCES_LIST
from ..types import Item
from ..parser.rss_feed_parser import RssFeedParser


class FeedGenerator:
    __sources_list: list[str] = SOURCES_LIST
    __title = 'MAIN'
    __link = 'http://example.com'
    __description = 'd'

    @classmethod
    def get_fg(cls) -> _FeedGenerator:
        fg = _FeedGenerator()
        fg.title(cls.__title)
        fg.link(href=cls.__link, rel='alternate')
        fg.description(cls.__description)
        return fg

    @classmethod
    def get_rss_feed(cls) -> str:
        fg = cls.get_fg()
        for source_url in cls.__sources_list:
            items = RssFeedParser.parse_from_url(source_url)
            for item in items:
                cls.__add_item_to_fg(fg, item)
        return fg.rss_str()

    @classmethod
    def __add_item_to_fg(cls, fg: _FeedGenerator, item: Item) -> None:
        fe = fg.add_item()
        fe.title(item.title)
        fe.content(item.text)
        fe.pubDate(item.date)
        fe.link(href='http://example.com', rel='alternate')
