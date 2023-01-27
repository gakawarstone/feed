from abc import ABC
from bs4 import BeautifulSoup
import logging
from datetime import timedelta

import requests

from app.services.cache.temporary import (
    TemporaryCacheService, UndefinedCache, ExpiredCache)
from app.services.cache.storage.memory import MemoryStorage
from ._base import BaseFeed as _BaseFeed


_headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        "AppleWebKit/537.36 (KHTML, like Gecko)"
        "Chrome/106.0.0.0 Safari/537.36"
    ),
}


# TODO: cache soup for constant time (example hour) or manually set

class WebParser(_BaseFeed, ABC):
    headers = _headers
    _cache_storage_time = timedelta(minutes=5)
    __cache: TemporaryCacheService[bytes] = TemporaryCacheService(
        storage=MemoryStorage()
    )

    @property
    def html(self) -> bytes:
        try:
            html = self.__cache.get(self.feed.url)
        except (UndefinedCache, ExpiredCache):
            logging.warning('making request to ' + self.feed.url)
            html = requests.get(self.feed.url, headers=self.headers).content
            self.__cache.set(self.feed.url, html, self._cache_storage_time)
        return html

    @property
    def soup(self) -> BeautifulSoup:
        return BeautifulSoup(self.html, 'html.parser')
