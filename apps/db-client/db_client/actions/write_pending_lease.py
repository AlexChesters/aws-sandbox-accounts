from aws_lambda_powertools import Logger

from db_client.utils.db import python_to_dynamo
from db_client.models.lease_status import LeaseStatus
from db_client.models.account_status import AccountStatus

logger = Logger()

def write_pending_lease(event, dynamo_client, table_name):
    params: dict = event.get("params")

    if not params:
        raise ValueError("'params' not provided in event")

    passed_properties = set(params.keys())
    expected_properties = set(["account_id", "lease_id", "user_id"])

    if passed_properties != expected_properties:
        logger.error(f"{passed_properties} is missing required properties")
        logger.error(f"expected properties: {expected_properties}")
        raise ValueError("'params' missing required properties")

    account_id = params["account_id"]
    lease_id = params["lease_id"]
    user_id = params["user_id"]

    get_items_response = dynamo_client.batch_get_item(
        RequestItems={
            table_name: {
                "Keys": [
                    python_to_dynamo({ "pk": "lease_status#pending" }),
                    python_to_dynamo({ "pk": "account_status#pending" })
                ]
            }
        }
    )

    existing_data = get_items_response["Responses"][table_name]

    pending_leases = LeaseStatus(
        next(item for item in existing_data if item["pk"]["S"] == "lease_status#pending")
    )
    pending_accounts = AccountStatus(
        next(item for item in existing_data if item["pk"]["S"] == "account_status#pending")
    )

    pending_leases.leases.add(lease_id)
    pending_accounts.accounts.add(account_id)

    dynamo_client.transact_write_items(
        TransactItems=[
            {
                "Put": {
                    "TableName": table_name,
                    "Item": pending_leases.to_dynamo()
                }
            },
            {
                "Put": {
                    "TableName": table_name,
                    "Item": pending_accounts.to_dynamo()
                }
            },
            {
                "Put": {
                    "TableName": table_name,
                    "Item": python_to_dynamo({
                        "pk": f"lease_id#{lease_id}",
                        "data": {
                            "state": "pending",
                            "account": account_id,
                            "user": user_id
                        }
                    })
                }
            }
        ]
    )

    return {
        "lease_id": lease_id,
        "account_id": account_id,
        "user_id": user_id
    }
