from fastapi import Response, Request
from services.generator import get_rss_feed


def show_rss(request: Request):
    return Response(content=get_rss_feed(), media_type="application/xml")
