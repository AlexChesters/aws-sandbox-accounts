from aws_sandbox_accounts_api.routers.accounts import router as accounts_router
from aws_sandbox_accounts_api.routers.leases import router as leases_router

__all__ = [
    "accounts_router",
    "leases_router"
]
