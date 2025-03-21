import time
import sys
import json

import boto3

from lease_manager.utils.step_function_status_poller import poll_for_step_function_status

sandbox_admin_session = boto3.Session(profile_name="sandbox-administrator")
step_functions = sandbox_admin_session.client("stepfunctions")

def create_lease(user_id: str, user_display_name: str, duration: str):
    start_response = step_functions.start_execution(
        # TODO: use live when it is ready
        stateMachineArn="arn:aws:states:eu-west-1:654654632738:stateMachine:test-aws-sandbox-accounts-lease-creator",
        input=json.dumps({
            "user_id": user_id,
            "duration": duration
        })
    )

    execution_arn = start_response["executionArn"]

    succeeded, final_status = poll_for_step_function_status(execution_arn)

    if succeeded:
        print(f"[SUCCESS] - lease successfully created for {user_display_name}")
        sys.exit(0)
    else:
        print(f"[ERROR] - error creating lease: {final_status}")
        sys.exit(1)
