from aws_lambda_powertools import Logger

from db_client.utils.db import python_to_dynamo
from db_client.models.lease_status import LeaseStatus

logger = Logger()

def remove_lease(event, dynamo_client, table_name):
    params: dict = event.get("params")

    if not params:
        raise ValueError("'params' not provided in event")

    passed_properties = set(params.keys())
    expected_properties = set(["account_id", "lease_id", "user_id"])

    if passed_properties != expected_properties:
        logger.error(f"{passed_properties} is missing required properties")
        logger.error(f"expected properties: {expected_properties}")
        raise ValueError("'params' missing required properties")

    lease_id = params["lease_id"]

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

    active_leases.leases.discard(lease_id)

    logger.info(active_leases)
