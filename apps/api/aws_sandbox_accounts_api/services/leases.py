import os
import json

import boto3

step_functions = boto3.Session(region_name="eu-west-1").client("stepfunctions")

def create_lease(*, user_id: str, duration: str) -> str:
    step_function_arn = os.getenv("LEASE_CREATOR_STEP_FUNCTION_ARN")

    start_response = step_functions.start_execution(
        stateMachineArn=step_function_arn,
        input=json.dumps({
            "user_id": user_id,
            "duration": duration
        })
    )

    execution_arn = start_response["executionArn"]

    return execution_arn
