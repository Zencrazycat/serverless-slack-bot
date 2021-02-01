import os

from aws_lambda_powertools import Logger
from lambda_decorators import dump_json_body

from src.handlers import send_markdown_message


logger = Logger(service="test-slack-bot")


@dump_json_body
@logger.inject_lambda_context(log_event=True)
def notify_about_new_vacation(event, _):
    record = event["Records"][0]
    if record["eventName"] == "INSERT" and record["dynamodb"]["Keys"]["sk"]["S"].startswith("VACATION"):
        new_vacation = record["dynamodb"]["NewImage"]
        text = f"@{new_vacation['username']['S']} booked *vacation* for the following dates:\n\n" \
               f"*{new_vacation['vacation_start_date']['S']} - {new_vacation['vacation_end_date']['S']}*\n\n" \
               f":palm_tree::airplane::sun_with_face::umbrella_on_ground:"
        slack_response = send_markdown_message(text, os.getenv("GENERAL_CHANNEL_ID"))
        logger.info(slack_response.json())
