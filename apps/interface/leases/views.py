import logging
from datetime import datetime, timezone

from django.http import HttpRequest
from django.shortcuts import render
import boto3
import humanize

from leases.utils.deserialise import deserialise
from leases.utils.get_user_details import get_user_details

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

        lease_raw_data = deserialise(lease_response)["data"]

        lease_data = lease_raw_data

        lease_data["user"] = get_user_details(lease_raw_data["user"])["UserName"]
        lease_data["lease_id"] = lease_id

        expiry_date = datetime.fromisoformat(lease_raw_data["expires"])
        expiry_date_formatted = expiry_date.strftime("%Y-%m-%d %H:%M:%S")
        expiry_date_natural = humanize.naturaltime(
            expiry_date.replace(tzinfo=timezone.utc),
            when=datetime.now(timezone.utc)
        )

        lease_data["expires"] = f"{expiry_date_formatted} ({expiry_date_natural})"

        active_leases.append(lease_data)

    context = {
        "active_leases": active_leases
    }

    logger.info({"message": "leases index context", "data": context})

    return render(request, "leases/index.html", context)
