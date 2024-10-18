import time
import sys
import json

import boto3

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

    while True:
        describe_response = step_functions.describe_execution(executionArn=execution_arn)
        status = describe_response["status"]

        match status:
            case "RUNNING":
                print("[INFO] - lease is pending creation, waiting 10 seconds")
            case "SUCCEEDED":
                print(f"[SUCCESS] - lease successfully created for {user_display_name}")
                sys.exit(0)
            case _:
                print(f"[ERROR] - error creating lease: {status}")
                sys.exit(1)

        time.sleep(10)
