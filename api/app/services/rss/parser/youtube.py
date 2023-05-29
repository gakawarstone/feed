from datetime import datetime, timedelta

import yt_dlp

from app.serializers.feed import Item
from app.services.cache.temporary import \
    TemporaryCacheService, UndefinedCache, ExpiredCache
from app.services.cache.storage.memory import MemoryStorage
from app.utils.datetime import convert_datetime
from ..exceptions import UnavailableFeed
from ._base import BaseFeed


class YoutubeFeed(BaseFeed):
    __cache: TemporaryCacheService[dict] = TemporaryCacheService(
        storage=MemoryStorage()
    )
    _cache_storage_time = timedelta(hours=1)
    _max_videos = 5
    _ydl_opts = {
        'ignoreerrors': True,
        'quiet': True,
        'extract_flat': True,
        'playlist_items': f'1-{_max_videos}'
    }

    @property
    async def items(self) -> list[Item]:
        try:
            channel_name = self._channel_name
            return [
                Item(
                    title='YT: ' + channel_name,
                    text=v['title'],
                    date=self._get_video_publish_date(v),
                    link=v['url'],
                )
                for v in self._videos
            ]
        except (UnavailableFeed, ValueError):
            return []

    def _get_video_publish_date(self, video: dict) -> datetime:
        info = self._get_page_info(video['url'])
        return convert_datetime(info['upload_date'])

    @property
    def _channel_name(self) -> str:
        info = self._get_page_info(self.feed.url)
        return info['uploader']

    @property
    def _videos(self) -> list[dict]:
        info = self._get_page_info(self.feed.url + '/videos')
        return info['entries']

    def _get_page_info(self, url: str) -> dict:
        try:
            info = self.__cache.get(url)
        except (UndefinedCache, ExpiredCache):
            with yt_dlp.YoutubeDL(self._ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
            self.__cache.set(url, info, self._cache_storage_time)
        if not info:
            raise ValueError
        return info
