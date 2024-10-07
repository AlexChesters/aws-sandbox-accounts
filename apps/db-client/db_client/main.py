import os

from aws_lambda_powertools import Logger, Tracer
import boto3

from db_client.actions.mark_as_dirty import mark_as_dirty
from db_client.actions.fetch_dirty import fetch_dirty
from db_client.actions.mark_as_available import mark_as_available
from db_client.actions.mark_as_failed import mark_as_failed
from db_client.actions.claim_available_account import claim_available_account
from db_client.actions.write_active_lease import write_active_lease
from db_client.actions.write_pending_lease import write_pending_lease
from db_client.actions.fetch_expired_leases import fetch_expired_leases
from db_client.actions.remove_leases import remove_leases

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
        case "fetch_dirty":
            return fetch_dirty(event, dynamodb, table_name)
        case "mark_as_available":
            return mark_as_available(event, dynamodb, table_name)
        case "mark_as_failed":
            return mark_as_failed(event, dynamodb, table_name)
        case "claim_available_account":
            return claim_available_account(event, dynamodb, table_name)
        case "write_active_lease":
            return write_active_lease(event, dynamodb, table_name)
        case "write_pending_lease":
            return write_pending_lease(event, dynamodb, table_name)
        case "fetch_expired_leases":
            return fetch_expired_leases(event, dynamodb, table_name)
        case "remove_leases":
            return remove_leases(event, dynamodb, table_name)
        case _:
            raise ValueError(f"'action' key value ({action}) provided was not recognised")
