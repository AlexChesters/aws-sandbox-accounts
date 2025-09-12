from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler.api_gateway import Router
from aws_lambda_powertools.event_handler import Response, content_types

from aws_sandbox_accounts_api.services import users as users_service

logger = Logger()
router = Router()

@router.get("/")
def get_all_users():
    users = users_service.get_all_users()

    return Response(
        status_code=200, content_type=content_types.APPLICATION_JSON, body=users
    )
