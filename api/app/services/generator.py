from .parser import parse_feed
from .config import fg

items = parse_feed('https://nitter.caioalonso.com/anthp86/rss')


def get_rss_feed() -> str:
    for item in items:
        fe = fg.add_item()
        fe.title(item.title)
        fe.content(item.text)
        # fe.pubDate(item.date) # FIXME with tz
        fe.link(href='http://example.com', rel='alternate')
    return fg.rss_str()
