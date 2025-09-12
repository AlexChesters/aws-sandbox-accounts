from aws_lambda_powertools import Logger

from aws_sandbox_accounts_api.models.account import Account, AccountStatus
from aws_sandbox_accounts_api.database_client import get_item

logger = Logger()

known_sandbox_accounts = {
    "227301199018": "testing",
    "905418121097": "alpha",
    "891377354273": "bravo",
    "471112670300": "charlie",
}

def get_all_accounts() -> list[Account]:
    results = {}

    for status in AccountStatus:
        accounts = get_item(pk=f"account_status#{status.value}")
        results[status] = []

        for account in accounts["data"]:
            if account not in known_sandbox_accounts:
                logger.error(f"Unknown account ID: {account}")
                raise Exception("Unknown account ID")

            results[status].append(Account(
                account_id=account,
                name=known_sandbox_accounts[account],
                status=status
            ).to_json())

    return results
