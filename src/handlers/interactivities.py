import datetime
import json
from urllib import parse

from aws_lambda_powertools import Logger
import holidays
from lambda_decorators import dump_json_body

from . import send_markdown_message, open_modal
from .modals import render_book_vacation_modal, render_see_user_vacations_modal
from .. import ValidationError
from ..services.aws.dynamodb import save_vacation_to_db, get_user_vacations_from_db, get_user_from_db


logger = Logger(service="test-slack-bot")

UA_HOLIDAYS = holidays.UA()
VACATION_DATES_FORMATTING = "%Y-%m-%d"
VACATION_DATES_FORMATTING_TO_DISPLAY = "%d.%m.%Y"

INTERACTIVITIES_RENDER_FUNCTIONS_MAPPING = {
    "book_vacation": render_book_vacation_modal,
    "see_user_vacations": render_see_user_vacations_modal,
}


def compute_working_days_in_vacation(start_date: datetime.datetime, end_date: datetime.datetime) -> int:
    vacation_dates_range = [start_date + datetime.timedelta(days=x) for x in range(0, (end_date - start_date).days)]
    working_days_count = 0
    for date in vacation_dates_range:
        if not (date.weekday() > 4 or date.strftime(VACATION_DATES_FORMATTING) in UA_HOLIDAYS):
            working_days_count += 1

    return working_days_count


def send_user_vacations(requster_user_id, interesting_user_id):
    user = get_user_from_db(interesting_user_id)
    username = user["username"] if user else "Selected user"
    user_vacations = get_user_vacations_from_db(interesting_user_id)
    if not user_vacations:
        text = f"{username} doesn't have booked vacations :thinking_face:"
    else:
        total_working_days = 0
        text = f"*@{username}* booked vacations:\n\n"
        for index, vacation in enumerate(user_vacations, 1):
            start_date = datetime.datetime.strptime(vacation["vacation_start_date"], VACATION_DATES_FORMATTING)
            end_date = datetime.datetime.strptime(vacation["vacation_end_date"], VACATION_DATES_FORMATTING)
            vacation_working_days = compute_working_days_in_vacation(start_date, end_date)
            total_working_days += vacation_working_days

            text += f"*{index}. " \
                    f"{start_date.strftime(VACATION_DATES_FORMATTING_TO_DISPLAY)} - " \
                    f"{end_date.strftime(VACATION_DATES_FORMATTING_TO_DISPLAY)}*\t\t" \
                    f"({vacation_working_days} working days)\n\n"

        text += f"Total working days: {total_working_days}"

    send_markdown_message(text, requster_user_id)


@dump_json_body
@logger.inject_lambda_context(log_event=True)
def process_interactivity(event, _):
    request_body_json = parse.parse_qs(event["body"])
    payload = json.loads(request_body_json["payload"][0])
    logger.info({"payload": payload})

    if interactivity_name := payload.get("callback_id"):
        render_modal_body_function = INTERACTIVITIES_RENDER_FUNCTIONS_MAPPING[interactivity_name]
        open_modal_body = render_modal_body_function(payload["trigger_id"])
        open_modal(open_modal_body)

    elif payload.get("type") == "view_submission":
        view = payload.get("view")
        if (callback_id := view["callback_id"]) == "book_vacation":
            block_data = view["state"]["values"]["vacation_dates"]
            try:
                save_vacation_to_db(
                    payload["user"]["id"],
                    payload["user"]["username"],
                    block_data["vacation_start_date"]["selected_date"],
                    block_data["vacation_end_date"]["selected_date"],
                )
                send_markdown_message(
                    "Vacation was booked *successfully* :stuck_out_tongue_winking_eye::+1:", payload["user"]["id"]
                )
            except ValidationError as e:
                send_markdown_message(
                    f"Vacation *was not booked*, because it is invalid: {e} :thinking_face:",
                    payload["user"]["id"]
                )

        elif callback_id == "see_user_vacations":
            block_data = view["state"]["values"]["user_selector"]
            send_user_vacations(payload["user"]["id"], block_data["user_selector"]["selected_user"])

    return {"statusCode": 200}
