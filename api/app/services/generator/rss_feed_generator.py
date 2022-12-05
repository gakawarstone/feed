from feedgen.feed import FeedGenerator as _FeedGenerator

from settings import SOURCES_LIST, SOURCES_DATA
from ..types import Item
from ..parser.rss_feed_parser import RssFeedParser
from ..parser.rezka_status_parser import RezkaShowFeedParser
from ..parser.tiktok_feed_parser import TiktokFeedParser


class FeedGenerator:
    __sources_list: list[str] = SOURCES_LIST
    __title = "MAIN"
    __link = "http://example.com"
    __description = "d"

    @classmethod
    def get_fg(cls) -> _FeedGenerator:
        fg = _FeedGenerator()
        fg.title(cls.__title)
        fg.link(href=cls.__link, rel="alternate")
        fg.description(cls.__description)
        return fg

    @classmethod
    def get_rss_feed(cls) -> str:
        fg = cls.get_fg()

        print('parsing newsletters')
        for source_url in cls.__sources_list:
            print('parsing url: ' + source_url)
            items = RssFeedParser.parse_from_url(source_url)
            for item in items:
                cls.__add_item_to_fg(fg, item)

        print('parsing rezka')
        for show_url in SOURCES_DATA["rezka"].values():
            for item in RezkaShowFeedParser().parse_show(show_url):
                cls.__add_item_to_fg(fg, item)

        print('parsing tiktok')
        for user_name in SOURCES_DATA["tiktok"].values():
            for item in TiktokFeedParser.parse_by_username(user_name):
                cls.__add_item_to_fg(fg, item)

        return fg.rss_str()

    @classmethod
    def __add_item_to_fg(cls, fg: _FeedGenerator, item: Item) -> None:
        fe = fg.add_item()
        fe.title(item.title)
        fe.content(item.text)
        fe.pubDate(item.date)
        fe.link(href=item.link, rel="alternate")
