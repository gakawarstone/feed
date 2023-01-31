from abc import ABC
from bs4 import BeautifulSoup
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


class WebParser(_BaseFeed, ABC):
    headers = _headers
    _cache_storage_time = timedelta(minutes=5)
    __cache: TemporaryCacheService[bytes] = TemporaryCacheService(
        storage=MemoryStorage()
    )

    def get_html(self, url: str) -> bytes:
        try:
            html = self.__cache.get(url)
        except (UndefinedCache, ExpiredCache):
            html = requests.get(url, headers=self.headers).content
            self.__cache.set(url, html, self._cache_storage_time)
        return html

    def get_soup(self, url: str) -> BeautifulSoup:
        return BeautifulSoup(self.get_html(url), 'html.parser')
