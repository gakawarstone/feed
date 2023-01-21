import os

from dotenv import load_dotenv


load_dotenv()


try:
    DB_URL = os.environ['DB_URL']
except ValueError:
    raise ValueError('Missing configuration')


MODELS = [
    'app.models.feed',
]
