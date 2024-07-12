from datetime import datetime, timedelta

from aws_lambda_powertools import Logger

from db_client.utils.db import python_to_dynamo
from db_client.models.lease_status import LeaseStatus
from db_client.models.account_status import AccountStatus

logger = Logger()

def remove_leases(event, dynamo_client, table_name):
    params: dict = event.get("params")

    if not params:
        raise ValueError("'params' not provided in event")

    for item in params["items"]:
        lease_id = item["lease_id"]
        account_id = item["account_id"]

        get_items_response = dynamo_client.batch_get_item(
            RequestItems={
                table_name: {
                    "Keys": [
                        python_to_dynamo({ "pk": "lease_status#active" }),
                        python_to_dynamo({ "pk": "account_status#leased" }),
                        python_to_dynamo({ "pk": "account_status#dirty" })
                    ]
                }
            }
        )

        existing_data = get_items_response["Responses"][table_name]

        active_leases = LeaseStatus(
            next(item for item in existing_data if item["pk"]["S"] == "lease_status#active")
        )
        leased_accounts = AccountStatus(
            next(item for item in existing_data if item["pk"]["S"] == "account_status#leased")
        )
        dirty_accounts = AccountStatus(
            next(item for item in existing_data if item["pk"]["S"] == "account_status#dirty")
        )

        active_leases.leases.discard(lease_id)
        leased_accounts.accounts.discard(account_id)
        dirty_accounts.accounts.add(account_id)

        # TODO: increase this to e.g. 2 weeks when not actively developing
        two_hours_from_now = datetime.now() + timedelta(hours=2)

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
                        "Item": leased_accounts.to_dynamo()
                    }
                },
                {
                    "Put": {
                        "TableName": table_name,
                        "Item": dirty_accounts.to_dynamo()
                    }
                },
                {
                    "Update": {
                        "TableName": table_name,
                        "Key": python_to_dynamo({
                            "pk": f"lease_id#{lease_id}"
                        }),
                        "UpdateExpression": "SET #data.#state = :expired, #data.#ttl = :ttl",
                        "ExpressionAttributeNames": {
                            "#data": "data",
                            "#state": "state",
                            "#ttl": "ttl"
                        },
                        "ExpressionAttributeValues": python_to_dynamo({
                            ":expired": "expired",
                            ":ttl": two_hours_from_now.timestamp()
                        })
                    }
                }
            ]
        )
