import datetime


def render_book_vacation_modal(trigger_id):
    today_string = str(datetime.date.today())
    return {
        "trigger_id": trigger_id,
        "view": {
            "callback_id": "book_vacation",
            "type": "modal",
            "title": {"type": "plain_text", "text": "Book a vacation", "emoji": True},
            "submit": {"type": "plain_text", "text": "Submit", "emoji": True},
            "close": {"type": "plain_text", "text": "Cancel", "emoji": True},
            "blocks": [
                {"type": "section", "text": {"type": "mrkdwn", "text": "*Please select the vacation start date:*"}},
                {
                    "type": "actions",
                    "block_id": "vacation_dates",
                    "elements": [
                        {"type": "datepicker", "initial_date": today_string, "action_id": "vacation_start_date"},
                        {"type": "datepicker", "initial_date": today_string, "action_id": "vacation_end_date"},
                    ],
                },
            ],
        },
    }


def render_see_user_vacations_modal(trigger_id):
    return {
        "trigger_id": trigger_id,
        "view": {
            "callback_id": "see_user_vacations",
            "type": "modal",
            "title": {"type": "plain_text", "text": "See vacations", "emoji": True},
            "submit": {"type": "plain_text", "text": "Submit", "emoji": True},
            "close": {"type": "plain_text", "text": "Cancel", "emoji": True},
            "blocks": [
                {
                    "type": "section",
                    "block_id": "user_selector",
                    "text": {"type": "mrkdwn", "text": "Pick a user to see his (her) vacations:"},
                    "accessory": {
                        "type": "users_select",
                        "action_id": "user_selector",
                        "placeholder": {"type": "plain_text", "text": "Select a user"},
                    },
                }
            ],
        },
    }
