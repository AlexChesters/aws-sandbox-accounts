from aws_sandbox_accounts_api.models.account import Account, AccountStatus
from aws_sandbox_accounts_api.database_client import get_item

def get_all_accounts() -> list[Account]:
    results = []

    for status in AccountStatus:
        accounts = get_item(f"account_status#{status.value}")
        results.extend(accounts)

    return results
