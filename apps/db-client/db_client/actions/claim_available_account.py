import random

from aws_lambda_powertools import Logger

from db_client.utils.db import python_to_dynamo
from db_client.models.account_status import AccountStatus

logger = Logger()

def claim_available_account(_event, dynamo_client, table_name):
    get_item_response = dynamo_client.get_item(
        TableName=table_name,
        Key=python_to_dynamo({
            "pk": "account_status#available"
        })
    )

    available_account = AccountStatus(get_item_response["Item"])

    if not available_account.accounts:
        raise RuntimeError("there are no available accounts")

    accounts = list(available_account.accounts)
    random.shuffle(accounts)
    claimed_account = accounts.pop()

    available_account.accounts = set(accounts)

    # TODO: write record back to db

    return claimed_account
