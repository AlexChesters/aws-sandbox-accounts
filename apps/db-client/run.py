from dataclasses import dataclass

import inquirer

from db_client import main

@dataclass
class LambdaContext:
    function_name: str = "aws-sandbox-accounts-db-client"
    memory_limit_in_mb: int = 128
    invoked_function_arn: str = "arn:aws:lambda:eu-west-1:111111111111:function:aws-sandbox-accounts-db-client"
    aws_request_id: str = "52fdfc07-2182-154f-163f-5f0f9a621d72"

events = {
    "mark_as_dirty": {
        "action": "mark_as_dirty",
        "params": {
            "account_id": "905418121097"
        }
    },
    "fetch_dirty": {
        "action": "fetch_dirty"
    }
}

answers = inquirer.prompt([
    inquirer.List(
        name="event",
        message="Choose an event",
        choices=list(events.keys())
    )
])

print(main.handler(events[answers["event"]], LambdaContext()))
