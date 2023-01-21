from abc import ABC
import requests
from bs4 import BeautifulSoup

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
    __cache: dict[str, BeautifulSoup] = {}

    @property
    def html(self) -> bytes:
        return requests.get(self.feed.url, headers=self.headers).content

    @property
    def soup(self) -> BeautifulSoup:
        return BeautifulSoup(self.html, 'html.parser')
