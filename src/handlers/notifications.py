import os

from aws_lambda_powertools import Logger
from lambda_decorators import dump_json_body


logger = Logger(service="test-slack-bot")

BOT_TOKEN = os.environ["BOT_TOKEN"]
OPEN_MODAL_URL = "https://slack.com/api/views.open"
SEND_MESSAGE_URL = "https://slack.com/api/chat.postMessage"


@dump_json_body
@logger.inject_lambda_context(log_event=True)
def notify_about_new_vacation(event, _):
    return event
