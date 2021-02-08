import os
import json

from aws_lambda_powertools import Logger


logger = Logger(service="test-slack-bot")

# Get Bot User OAuth Access token from environment
BOT_TOKEN = os.environ["BOT_TOKEN"]
# Slack URL to send bot replies
SLACK_URL = "https://slack.com/api/chat.postMessage"


def process_message(event, _):
    logger.info("Request Event: {}".format(event))
    if "body" in event:
        request_body_json = json.loads(event["body"])
        logger.info("Received API Gateway Request with Body: {}".format(request_body_json))
        if challenge := request_body_json.get("challenge"):
            # For verification by Slack
            logger.info("Challenge: {}".format(challenge))
            challenge_response = dict()
            challenge_response["challenge"] = challenge
            response = {"statusCode": 200, "body": json.dumps(challenge_response)}
            return response

    return {"statusCode": 200}

