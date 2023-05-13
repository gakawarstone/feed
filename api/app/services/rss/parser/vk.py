from datetime import timedelta, datetime, date

from bs4 import Tag

from app.utils.datetime import convert_datetime, constant_datetime
from app.serializers.feed import Item
from ..exceptions import UnavailableFeed
from ._parser import WebParser


class VkFeed(WebParser):
    _cache_storage_time = timedelta(seconds=1)

    @property
    async def items(self) -> list[Item]:
        try:
            return [
                Item(
                    title=self._get_post_title(p),
                    text=self._get_post_text(p),
                    date=self._get_post_datetime(p),
                    link=self._get_post_link(p),
                )
                for p in self._posts
            ]
        except (UnavailableFeed, ValueError):
            return []

    @property
    def _posts(self) -> list[Tag]:
        soup = self.get_soup(self.feed.url)
        return [p for p in soup.find_all(class_='post')]

    def _get_post_title(self, post: Tag) -> str:
        try:
            return post.find_all(class_='PostHeaderTitle__authorName')[0].text
        except IndexError:
            raise ValueError

    def _get_post_text(self, post: Tag) -> str:
        try:
            return post.find_all(class_='wall_post_text')[0].text
        except IndexError:
            raise ValueError

    def _get_post_datetime(self, post: Tag) -> datetime:
        try:
            datetime_str = post.find_all('time')[0].text
            return self._parse_datetime(datetime_str)
        except IndexError:
            raise ValueError

    def _parse_datetime(self, datetime_str: str) -> datetime:
        if datetime_str.startswith('today'):
            today_str = date.today().strftime('%m/%d/%Y')
            datetime_str = today_str + datetime_str.split('at')[1]

        if datetime_str.startswith('yesterday'):
            yesterday = date.today() - timedelta(days=1)
            yesterday_str = yesterday.strftime('%m/%d/%Y')
            datetime_str = yesterday_str + datetime_str.split('at')[1]

        try:
            return convert_datetime(datetime_str)
        except Exception as e:
            print(e)
            return constant_datetime

    def _get_post_link(self, post: Tag) -> str:
        try:
            link = post.find_all(class_='post_link')[0]['href']
            if not link.startswith('https'):
                link = 'https://vk.com' + link
            link = link.split('?')[0]
            return link
        except IndexError:
            raise ValueError