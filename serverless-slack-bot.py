import os
import json
from urllib import parse

from aws_lambda_powertools import Logger
import requests


logger = Logger(service="test-slack-bot")

# Get Bot User OAuth Access token from environment
BOT_TOKEN = os.environ["BOT_TOKEN"]

# Slack URL to send bot replies
SLACK_URL = "https://slack.com/api/chat.postMessage"


def handler(event, context):
    logger.info("Request Event: {}".format(event))
    try:
        # Default empty response
        response = dict()
        if 'body' in event:
            request_body_json = event['body']
            logger.info('Received API Gateway Request with Body: {}'.format(request_body_json))
            if 'challenge' in request_body_json:
                # For verification by Slack
                challenge = request_body_json["challenge"]
                logger.info('Challenge: {}'.format(challenge))
                challenge_response = dict()
                challenge_response['challenge'] = challenge
                response = {
                    'status_code': 200,
                    'body': json.dumps(challenge_response)
                }

            if 'event' in request_body_json:
                slack_event = request_body_json['event']
                logger.info('Received Slack Event with Body: {}'.format(slack_event))
                if 'bot_id' in slack_event:
                    logger.warn('Ignored bot event')
                else:
                    user_message = slack_event['text']
                    logger.info('User Message: {}'.format(user_message))

                    # Create your Bot Reply logic here
                    # For now - this is a hardcoded reply
                    """In ideal cases - configure a NLP service like Watson Assistant or Rasa NLU
                    to respond to a natural languages user text"""
                    bot_reply = "Hello I am the Serverless Slack Bot"

                    # Get the ID of the channel where the message was posted.
                    channel_id = slack_event["channel"]

                    if len(user_message) > 0:
                        # Create an associative array and URL-encode it
                        # The Slack API doesn't not handle JSON
                        data = parse.urlencode(
                            (
                                ("token", BOT_TOKEN),
                                ("channel", channel_id),
                                ("text", bot_reply)
                            )
                        )
                        data = data.encode("ascii")
                        requests.post(
                            SLACK_URL, data=data, headers={"Content-type": "application/x-www-form-urlencoded"}
                        )

                        # Construct the HTTP request that will be sent to the Slack API.
                        # request = urllib.request.Request(
                        #     SLACK_URL,
                        #     data=data,
                        #     method="POST"
                        # )
                        #
                        # # Add a header mentioning that the text is URL-encoded.
                        # request.add_header(
                        #     "Content-Type",
                        #     "application/x-www-form-urlencoded"
                        # )
                        #
                        # # Fire the request
                        # urllib.request.urlopen(request).read()

                        # Success
                        response = {
                            'status_code': 200,
                        }
        logger.info("Response: {}".format(response))
        return response
    except Exception as e:
        # Error
        logger.error(e)
