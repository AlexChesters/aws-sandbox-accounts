from aws_lambda_powertools import Logger

from db_client.utils.db import python_to_dynamo
from db_client.models.lease_status import LeaseStatus

logger = Logger()

def fetch_expired_leases(_event, dynamo_client, table_name):
    get_item_response = dynamo_client.get_item(
        TableName=table_name,
        Key=python_to_dynamo({
            "pk": "lease_status#active"
        })
    )

    active_leases = LeaseStatus(get_item_response["Item"])

    get_items_response = dynamo_client.batch_get_item(
        RequestItems={
            table_name: {
                "Keys": [
                    python_to_dynamo({ "pk": f"lease_id#{lease_id}" })
                    for lease_id in active_leases.leases
                ]
            }
        }
    )
    items = get_items_response["Responses"][table_name]

    for item in items:
        logger.info(item)

    return {}
