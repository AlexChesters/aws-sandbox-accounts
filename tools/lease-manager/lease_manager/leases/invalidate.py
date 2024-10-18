from datetime import datetime, timedelta, timezone

import boto3

from lease_manager.utils.deserialise import deserialise
from lease_manager.utils.serialise import serialise

sandbox_admin_session = boto3.Session(profile_name="sandbox-administrator")
dynamo = sandbox_admin_session.client("dynamodb")

def invalidate_lease(lease_id: str):
    lease_response = dynamo.query(
        TableName="test-aws-sandbox-accounts-account-pool",
        KeyConditionExpression="pk = :pk_val",
        ExpressionAttributeValues={":pk_val": {"S": f"lease_id#{lease_id}"}}
    )

    lease = deserialise(lease_response)

    lease["data"]["expires"] = (datetime.now(timezone.utc) - timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]

    dynamo.put_item(
        TableName="test-aws-sandbox-accounts-account-pool",
        Item={
            "pk": {"S": f"lease_id#{lease_id}"},
            "data": {"M": serialise(lease["data"])}
        }
    )

    print(f"[SUCCESS] - lease {lease_id} has been invalidated")
