import os

from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler import APIGatewayHttpResolver, CORSConfig
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools.utilities.typing import LambdaContext

from aws_sandbox_accounts_api.routers import accounts_router, leases_router

environment = os.getenv("ENVIRONMENT", "live")

logger = Logger()
cors_config = CORSConfig(
    allow_origin="https://test.sandbox.alexchesters.com" if environment == "test" else "https://sandbox.alexchesters.com",
    extra_origins=["http://localhost:5173/"] if environment == "test" else [],
    allow_headers=["authorization", "client"],
    allow_credentials=True,
    max_age=60
)
app = APIGatewayHttpResolver(cors=cors_config)

app.include_router(accounts_router, prefix="/accounts")
app.include_router(leases_router, prefix="/leases")

@logger.inject_lambda_context(log_event=True, correlation_id_path=correlation_paths.API_GATEWAY_HTTP)
def handler(event: dict, context: LambdaContext) -> dict:
    return app.resolve(event, context)
