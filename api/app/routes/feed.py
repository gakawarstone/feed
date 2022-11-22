from fastapi import Response, Request
from services.generator.rss_feed_generator import FeedGenerator


def show_rss(request: Request):
    content = FeedGenerator.get_rss_feed()
    return Response(content=content, media_type="application/xml")
