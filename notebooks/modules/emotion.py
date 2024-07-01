import os
from dotenv import load_dotenv

import requests

load_dotenv()

LANG = 'es'
APIKEY = os.getenv("APIKEY")
APIURL = 'https://sentic.net/api/' + LANG + '/' + APIKEY + '.py?text='


def get_emotion(text: str):
    response = requests.get(APIURL + text)
    return response
