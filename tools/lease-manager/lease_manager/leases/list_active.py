from datetime import datetime, timezone

import boto3
from rich.console import Console
from rich.table import Table
import humanize

from lease_manager.utils.deserialise import deserialise
from lease_manager.identities.user_details import get_user_details

sandbox_admin_session = boto3.Session(profile_name="sandbox-administrator", region_name="eu-west-1")
dynamo = sandbox_admin_session.client("dynamodb")

def _print_leases(leases):
    table = Table(title="Active leases", show_header=True)
    table.add_column("Lease ID")
    table.add_column("User")
    table.add_column("Account ID")
    table.add_column("Expires")

    for lease_id, lease_data in leases.items():
        expiry_date = datetime.fromisoformat(lease_data["expires"])
        user = get_user_details(lease_data["user"])

        expiry_iso = expiry_date.isoformat()
        expiry_human = humanize.naturaltime(
            expiry_date.replace(tzinfo=timezone.utc),
            when=datetime.now(timezone.utc)
        )

        table.add_row(
            lease_id,
            user["UserName"],
            lease_data["account"],
            f"{expiry_iso} ({expiry_human})"
        )

    console = Console()
    console.print(table)

def list_active_leases():
    active_leases_response = dynamo.query(
        TableName="test-aws-sandbox-accounts-account-pool",
        KeyConditionExpression="pk = :pk_val",
        ExpressionAttributeValues={":pk_val": {"S": "lease_status#active"}}
    )

    active_leases = deserialise(active_leases_response)
    active_leases_data = {}

    for lease_id in active_leases["data"]:
        lease_response = dynamo.query(
            TableName="test-aws-sandbox-accounts-account-pool",
            KeyConditionExpression="pk = :pk_val",
            ExpressionAttributeValues={":pk_val": {"S": f"lease_id#{lease_id}"}}
        )

        active_leases_data[lease_id] = deserialise(lease_response)["data"]

    _print_leases(active_leases_data)
