from dataclasses import dataclass
from datetime import datetime


@dataclass
class Item:
    title: str
    text: str
    date: datetime
    link: str
