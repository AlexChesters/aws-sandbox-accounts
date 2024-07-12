from aws_lambda_powertools import Logger, Tracer
import boto3

from auth_client.actions.create_lease import create_lease

logger = Logger()
tracer = Tracer()

@tracer.capture_lambda_handler
@logger.inject_lambda_context(log_event=True)
def handler(event, _context):
    action = event.get("action")

    if not action:
        raise ValueError("'action' key not provided in event")

    sso_client = boto3.client("sso-admin")

    match action:
        case "create_lease":
            return create_lease(event, sso_client)
        case _:
            raise ValueError(f"'action' key value ({action}) provided was not recognised")
