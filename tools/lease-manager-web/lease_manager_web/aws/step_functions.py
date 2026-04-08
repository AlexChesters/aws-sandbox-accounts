import json
import time

import lease_manager_web.aws.sessions as sessions

LEASE_CREATOR_ARN = "arn:aws:states:eu-west-1:654654632738:stateMachine:live-aws-sandbox-accounts-lease-creator"
LEASE_JANITOR_ARN = "arn:aws:states:eu-west-1:654654632738:stateMachine:live-aws-sandbox-accounts-lease-janitor"


def start_and_poll(
    state_machine_arn: str, input_payload: dict | None = None
) -> tuple[bool, str | None]:
    kwargs = {"stateMachineArn": state_machine_arn}
    if input_payload is not None:
        kwargs["input"] = json.dumps(input_payload)

    sf = sessions.step_functions()
    start_response = sf.start_execution(**kwargs)
    execution_arn = start_response["executionArn"]

    while True:
        describe_response = sf.describe_execution(executionArn=execution_arn)
        status = describe_response["status"]

        if status == "SUCCEEDED":
            return True, None
        elif status != "RUNNING":
            return False, status

        time.sleep(10)
