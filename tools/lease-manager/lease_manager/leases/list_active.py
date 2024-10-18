import boto3
from rich.console import Console
from rich.table import Table

from lease_manager.utils.deserialise import deserialise

sandbox_admin_session = boto3.Session(profile_name="sandbox-administrator")
dynamo = sandbox_admin_session.client("dynamodb")

def _print_leases(leases):
    table = Table(title="Active leases", show_header=True)
    table.add_column("User ID")
    table.add_column("Account ID")
    table.add_column("Expires")

    for lease in leases:
        table.add_row(lease["user"], lease["account"], lease["expires"])

    console = Console()
    console.print(table)

def list_active_leases():
    active_leases_response = dynamo.query(
        TableName="test-aws-sandbox-accounts-account-pool",
        KeyConditionExpression="pk = :pk_val",
        ExpressionAttributeValues={":pk_val": {"S": "lease_status#active"}}
    )

    active_leases = deserialise(active_leases_response)
    active_leases_data = []

    for lease_id in active_leases["data"]:
        lease_response = dynamo.query(
            TableName="test-aws-sandbox-accounts-account-pool",
            KeyConditionExpression="pk = :pk_val",
            ExpressionAttributeValues={":pk_val": {"S": f"lease_id#{lease_id}"}}
        )

        active_leases_data.append(deserialise(lease_response)["data"])

    _print_leases(active_leases_data)
