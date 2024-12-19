import logging

from django.http import HttpRequest
from django.shortcuts import render
import boto3

from leases.utils.deserialise import deserialise

logger = logging.getLogger(__name__)

sandbox_admin_session = boto3.Session(profile_name="sandbox-administrator")
dynamo = sandbox_admin_session.client("dynamodb")

def index(request: HttpRequest):
    active_leases_response = dynamo.query(
        TableName="test-aws-sandbox-accounts-account-pool",
        KeyConditionExpression="pk = :pk_val",
        ExpressionAttributeValues={":pk_val": {"S": "lease_status#active"}}
    )

    active_leases = []

    for lease_id in deserialise(active_leases_response)["data"]:
        lease_response = dynamo.query(
            TableName="test-aws-sandbox-accounts-account-pool",
            KeyConditionExpression="pk = :pk_val",
            ExpressionAttributeValues={":pk_val": {"S": f"lease_id#{lease_id}"}}
        )

        lease_data = deserialise(lease_response)["data"]
        lease_data["lease_id"] = lease_id

        active_leases.append(lease_data)

    context = {
        "active_leases": active_leases
    }

    logger.info({"message": "leases index context", "data": context})

    return render(request, "leases/index.html", context)
