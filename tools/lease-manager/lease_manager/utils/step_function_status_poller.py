import time

import boto3

sandbox_admin_session = boto3.Session(profile_name="sandbox-administrator", region_name="eu-west-1")
step_functions = sandbox_admin_session.client("stepfunctions")

def poll_for_step_function_status(execution_arn: str) -> int:
    while True:
        describe_response = step_functions.describe_execution(executionArn=execution_arn)
        status = describe_response["status"]

        match status:
            case "RUNNING":
                print("[INFO] - polling step function, waiting 10 seconds")
            case "SUCCEEDED":
                return True, None
            case _:
                return False, status

        time.sleep(10)
