from aws_lambda_powertools import Logger

from account_manager_db_client.utils.db import python_to_dynamo
from account_manager_db_client.models.account_status import AccountStatus

logger = Logger()

def mark_as_initial(event, dynamo_client, table_name):
    account_id = event.get("params", {}).get("account_id")

    if not account_id:
        raise ValueError("'params.account_id' not provided in event")

    get_items_response = dynamo_client.batch_get_item(
        RequestItems={
            table_name: {
                "Keys": [
                    python_to_dynamo({ "pk": "account_status#all" }),
                    python_to_dynamo({ "pk": "account_status#available" }),
                    python_to_dynamo({ "pk": "account_status#leased" }),
                    python_to_dynamo({ "pk": "account_status#initial" })
                ]
            }
        }
    )

    existing_data = get_items_response["Responses"][table_name]

    all_accounts = AccountStatus(
        next(item for item in existing_data if item["pk"]["S"] == "account_status#all")
    )
    available_accounts = AccountStatus(
        next(item for item in existing_data if item["pk"]["S"] == "account_status#available")
    )
    leased_accounts = AccountStatus(
        next(item for item in existing_data if item["pk"]["S"] == "account_status#leased")
    )
    initial_accounts = AccountStatus(
        next(item for item in existing_data if item["pk"]["S"] == "account_status#initial")
    )

    all_accounts.accounts.add(account_id)
    initial_accounts.accounts.add(account_id)
    available_accounts.accounts.discard(account_id)
    leased_accounts.accounts.discard(account_id)

    dynamo_client.transact_write_items(
        TransactItems=[
            {
                "Put": {
                    "TableName": table_name,
                    "Item": all_accounts.to_dynamo()
                }
            },
            {
                "Put": {
                    "TableName": table_name,
                    "Item": initial_accounts.to_dynamo()
                }
            },
            {
                "Put": {
                    "TableName": table_name,
                    "Item": available_accounts.to_dynamo()
                }
            },
            {
                "Put": {
                    "TableName": table_name,
                    "Item": leased_accounts.to_dynamo()
                }
            }
        ]
    )

    return {
        "account_id": account_id
    }
