from aws_lambda_powertools import Logger

from db_client.utils.db import python_to_dynamo
from db_client.models.account_status import AccountStatus

logger = Logger()

def fetch_dirty(_event, dynamo_client, table_name):
    get_item_response = dynamo_client.get_item(
        TableName=table_name,
        Key=python_to_dynamo({
            "pk": "account_status#dirty"
        })
    )

    dirty_status = AccountStatus(get_item_response["Item"])

    return list(dirty_status.accounts)
