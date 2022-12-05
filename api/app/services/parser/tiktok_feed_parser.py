from fastapi.logger import logger

from .rss_feed_parser import RssFeedParser
from ..types import Item


class TiktokFeedParser(RssFeedParser):
    __base_url = "https://rsshub.app/tiktok/user/@"

    @classmethod
    def parse_by_username(cls, user_name: str) -> list[Item]:
        logger.warning("parsing tiktok: @" + user_name)
        return cls.parse_from_url(cls.__base_url + user_name)
