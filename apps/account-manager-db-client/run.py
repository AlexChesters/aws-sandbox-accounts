from dataclasses import dataclass

from account_manager_db_client import main

@dataclass
class LambdaContext:
    function_name: str = "aws-sandbox-accounts-account-manager-db-client"
    memory_limit_in_mb: int = 128
    invoked_function_arn: str = "arn:aws:lambda:eu-west-1:111111111111:function:aws-sandbox-accounts-account-manager-db-client"
    aws_request_id: str = "52fdfc07-2182-154f-163f-5f0f9a621d72"

event = {
    "action": "mark_as_dirty",
    "params": {
        "account_id": "905418121097"
    }
}

main.handler(event, LambdaContext())
