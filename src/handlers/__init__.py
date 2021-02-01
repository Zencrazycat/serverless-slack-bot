import os

import requests


BOT_TOKEN = os.environ["BOT_TOKEN"]
OPEN_MODAL_URL = "https://slack.com/api/views.open"
SEND_MESSAGE_URL = "https://slack.com/api/chat.postMessage"


def send_markdown_message(text, channel):
    send_user_vacations_body = {
        "channel": channel,
        "blocks": [{"type": "section", "text": {"type": "mrkdwn", "text": text}}],
    }
    slack_response = requests.post(
        SEND_MESSAGE_URL, headers={"Authorization": f"Bearer {BOT_TOKEN}"}, json=send_user_vacations_body
    )
    return slack_response


def open_modal(open_modal_body):
    requests.post(OPEN_MODAL_URL, headers={"Authorization": f"Bearer {BOT_TOKEN}"}, json=open_modal_body)
