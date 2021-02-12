import os

import requests
from aws_lambda_powertools import Logger
from lambda_decorators import load_json_body, dump_json_body


logger = Logger(service="HR-slack-bot")


BOT_TOKEN = os.environ["BOT_TOKEN"]
SEND_MESSAGE_URL = "https://slack.com/api/chat.postMessage"
SLACK_URL = "https://slack.com/api/chat.postMessage"


@logger.inject_lambda_context(log_event=True)
@load_json_body
@dump_json_body
def process_message(event, _):
    if request_body_json := event.get("body"):
        if challenge := request_body_json.get("challenge"):
            # For verification by Slack
            logger.info(f"Challenge: {challenge}")
            response = {"statusCode": 200, "body": {"challenge": challenge}}
            return response

    return {"statusCode": 200}


def send_markdown_message(text, channel=None, webhook_url=None):
    body = {"blocks": [{"type": "section", "text": {"type": "mrkdwn", "text": text}}]}
    if channel:
        body["channel"] = channel
        slack_response = requests.post(SEND_MESSAGE_URL, headers={"Authorization": f"Bearer {BOT_TOKEN}"}, json=body)
    else:
        slack_response = requests.post(webhook_url, json=body)
    logger.info(slack_response.json())
    return slack_response
