from datetime import datetime, timedelta, timezone
import sys

import boto3

from lease_manager.utils.deserialise import deserialise
from lease_manager.utils.serialise import serialise
from lease_manager.utils.step_function_status_poller import poll_for_step_function_status

sandbox_admin_session = boto3.Session(profile_name="sandbox-administrator", region_name="eu-west-1")
dynamo = sandbox_admin_session.client("dynamodb")
step_functions = sandbox_admin_session.client("stepfunctions")

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

    print(f"[INFO] - database has been updated, starting janitor step function")

    start_response = step_functions.start_execution(
        # TODO: use live when it is ready
        stateMachineArn="arn:aws:states:eu-west-1:654654632738:stateMachine:test-aws-sandbox-accounts-lease-janitor",
    )

    execution_arn = start_response["executionArn"]

    succeeded, final_status = poll_for_step_function_status(execution_arn)

    if succeeded:
        print(f"[SUCCESS] - lease {lease_id} has been invalidated")
        sys.exit(0)
    else:
        print(f"[ERROR] - error creating lease: {final_status}")
        sys.exit(1)
