import os

import requests


BOT_TOKEN = os.environ["BOT_TOKEN"]
OPEN_MODAL_URL = "https://slack.com/api/views.open"


def open_modal(open_modal_body):
    requests.post(OPEN_MODAL_URL, headers={"Authorization": f"Bearer {BOT_TOKEN}"}, json=open_modal_body)
