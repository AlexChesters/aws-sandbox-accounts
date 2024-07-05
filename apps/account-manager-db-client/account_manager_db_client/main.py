import os

from aws_lambda_powertools import Logger, Tracer
import boto3

from account_manager_db_client.actions.mark_as_dirty import mark_as_dirty

table_name = os.environ["TABLE_NAME"]

logger = Logger()
tracer = Tracer()

@tracer.capture_lambda_handler
@logger.inject_lambda_context(log_event=True)
def handler(event, _context):
    action = event.get("action")

    if not action:
        raise ValueError("'action' key not provided in event")

    dynamodb = boto3.client("dynamodb")

    match action:
        case "mark_as_dirty":
            return mark_as_dirty(event, dynamodb, table_name)
        case _:
            raise ValueError(f"'action' key value ({action}) provided was not recognised")
