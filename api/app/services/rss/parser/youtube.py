from datetime import datetime, timedelta

import yt_dlp

from app.serializers.feed import Item
from app.services.cache.use_temporary import (
    UseTemporaryCacheServiceExtension, async_store_in_cache_for)
from app.utils.datetime import convert_datetime
from app.utils.async_wrapper import async_wrap
from ..exceptions import UnavailableFeed
from ._base import BaseFeed


class YoutubeFeed(BaseFeed, UseTemporaryCacheServiceExtension[dict]):
    _channel_info_storage_time = timedelta(hours=1)
    _video_info_storage_time = timedelta(weeks=1)
    _max_videos = 5
    _ydl_opts_tab = {
        'ignoreerrors': True,
        'quiet': True,
        'lazy_playlist': False,
        'extract_flat': True,
        'playlist_items': f'1-{_max_videos}',
        'extractor_args': {'youtubetab': {
            'approximate_date': 'upload_date',
        }},
    }
    _ydl_opts_video = {
        'ignoreerrors': True,
        'quiet': True,
        'extract_flat': False,
        'skip_download': True,
        'extractorargs': {
            'youtube': {
                'player_skip': ['js', 'webpage', 'configs'],
                'skip': ['hls', 'dash', 'translated_tabs'],
            }
        }
    }

    @property
    async def items(self) -> list[Item]:
        try:
            channel_name = await self._channel_name
            return [
                Item(
                    title='YT: ' + channel_name,
                    text=v['title'],
                    date=await self._get_video_publish_date(v),
                    link=v['url'],
                )
                for v in await self._videos
            ]
        except (UnavailableFeed, ValueError):
            return []

    async def _get_video_publish_date(self, video: dict) -> datetime:
        yesterday = datetime.today() - timedelta(days=1)
        if video['timestamp'] and video['timestamp'] >= yesterday.timestamp():
            date_str = datetime.fromtimestamp(
                video['timestamp']).strftime('%Y%m%d')
            return convert_datetime(date_str)
        info = await self._get_video_info(video['url'])
        return convert_datetime(info['upload_date'])

    @property
    async def _channel_name(self) -> str:
        info = await self._get_page_info(self.feed.url + '/videos')
        return info['uploader']

    @property
    async def _videos(self) -> list[dict]:
        info = await self._get_page_info(self.feed.url + '/videos')
        return info['entries']

    @async_store_in_cache_for(_video_info_storage_time)
    async def _get_video_info(self, url: str) -> dict:
        return await self._get_page_info(url, self._ydl_opts_video)

    @async_store_in_cache_for(_channel_info_storage_time)
    @async_wrap
    def _get_page_info(self, url: str, opts: dict = _ydl_opts_tab) -> dict:
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=False)
        if not info:
            raise ValueError
        return info
