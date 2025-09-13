from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler.api_gateway import Router
from aws_lambda_powertools.event_handler import Response, content_types
from pydantic import BaseModel, ValidationError
from aws_lambda_powertools.utilities.parser import parse

from aws_sandbox_accounts_api.services import leases as leases_service

logger = Logger()
router = Router()

class LeaseRequest(BaseModel):
    user_id: str
    duration: str

@router.post("/")
def create_lease():
    try:
        lease_request = parse(event=router.current_event.json_body, model=LeaseRequest)
    except ValidationError as e:
        logger.error(f"Validation error: {e}")
        return Response(
            status_code=400,
            content_type=content_types.APPLICATION_JSON,
            body={"error": "Invalid request", "details": e.errors()},
        )

    execution_arn = leases_service.create_lease(lease_request.user_id, lease_request.duration)

    return Response(
        status_code=202, content_type=content_types.APPLICATION_JSON, body={"execution_arn": execution_arn}
    )
