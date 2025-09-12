from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler.api_gateway import Router
from aws_lambda_powertools.event_handler import Response, content_types

from aws_sandbox_accounts_api.services import leases as leases_service

logger = Logger()
router = Router()

@router.post("/")
def create_lease():
    leases_service.create_lease()

    return Response(
        status_code=202, content_type=content_types.APPLICATION_JSON, body={}
    )
