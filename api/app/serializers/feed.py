from datetime import datetime

from pydantic import BaseModel


class Feed(BaseModel):
    title: str
    url: str
    type: str


class Item(BaseModel):
    title: str
    text: str
    date: datetime
    link: str
