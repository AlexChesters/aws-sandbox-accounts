from aws_lambda_powertools import Logger

from db_client.utils.db import python_to_dynamo
from db_client.models.lease_status import LeaseStatus

logger = Logger()

def write_lease(event, dynamo_client, table_name):
    account_id = event.get("params", {}).get("account_id")
    lease_id = event.get("params", {}).get("lease_id")
    user_id = event.get("params", {}).get("user_id")

    if not account_id:
        raise ValueError("'params.account_id' not provided in event")

    if not lease_id:
        raise ValueError("'params.lease_id' not provided in event")

    if not user_id:
        raise ValueError("'params.user_id' not provided in event")

    get_items_response = dynamo_client.batch_get_item(
        RequestItems={
            table_name: {
                "Keys": [
                    python_to_dynamo({ "pk": "lease_status#active" })
                ]
            }
        }
    )

    existing_data = get_items_response["Responses"][table_name]

    active_leases = LeaseStatus(
        next(item for item in existing_data if item["pk"]["S"] == "lease_status#active")
    )

    active_leases.accounts.add(account_id)

    dynamo_client.transact_write_items(
        TransactItems=[
            {
                "Put": {
                    "TableName": table_name,
                    "Item": active_leases.to_dynamo()
                }
            },
            {
                "Put": {
                    "TableName": table_name,
                    "Item": python_to_dynamo({
                        "pk": f"lease_id#{lease_id}",
                        "data": {
                            "state": "active",
                            "account": account_id,
                            "user": user_id
                        }
                    })
                }
            }
        ]
    )
