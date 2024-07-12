from aws_lambda_powertools import Logger

from db_client.utils.db import python_to_dynamo
from db_client.models.lease_status import LeaseStatus

logger = Logger()

def write_lease(event, dynamo_client, table_name):
    params: dict = event.get("params")

    if not params:
        raise ValueError("'params' not provided in event")

    passed_properties = set(params.keys())
    expected_properties = set(["account_id", "lease_id", "user_id", "expiry"])

    if passed_properties != expected_properties:
        logger.error(f"{passed_properties} is missing required properties")
        logger.error(f"expected properties: {expected_properties}")
        raise ValueError("'params' missing required properties")

    account_id = params["account_id"]
    lease_id = params["lease_id"]
    user_id = params["user_id"]
    expiry = params["expiry"]

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
                            "user": user_id,
                            "expiry": expiry
                        }
                    })
                }
            }
        ]
    )
