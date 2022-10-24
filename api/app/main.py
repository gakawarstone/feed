from fastapi import FastAPI, Response
from generator import get_rss_feed

app = FastAPI()


@app.route('/feed')
def show_rss(request):
    return Response(content=get_rss_feed(), media_type="application/xml")
