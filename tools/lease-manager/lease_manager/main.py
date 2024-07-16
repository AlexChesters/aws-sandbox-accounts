import json

import boto3
import inquirer

from lease_manager.utils.flatten import flatten

management_session = boto3.Session(profile_name="management")
sandbox_admin_session = boto3.Session(profile_name="sandbox-administrator")

identity_store = management_session.client("identitystore")
step_functions = sandbox_admin_session.client("stepfunctions")

list_users_paginator = identity_store.get_paginator("list_users")

results = list_users_paginator.paginate(IdentityStoreId="d-93677ee9b2")
flat_results = flatten(result["Users"] for result in results)
users = [(user["UserName"], user["UserId"]) for user in flat_results]
durations = [
    ("5 minutes", "5m"),
    ("30 minutes", "30m"),
    ("1 hour", "1h"),
    ("3 hours", "3h"),
    ("6 hours", "6h"),
    ("12 hours", "12h"),
    ("24 hours", "24h")
]

answers = inquirer.prompt([
    inquirer.List(
        "user",
        message="Which user do you want to create a lease for?",
        choices=users
    ),
    inquirer.List(
        "duration",
        message="How long should the lease last?",
        choices=durations
    )
])

chosen_user_display_name, chosen_user_id = next(user for user in users if user[1] == answers["user"])
chosen_duration_display, chosen_duration_value = next(duration for duration in durations if duration[1] == answers["duration"])

response = step_functions.start_execution(
    # TODO: use live when it is ready
    stateMachineArn="arn:aws:states:eu-west-1:654654632738:stateMachine:test-aws-sandbox-accounts-lease-creator",
    input=json.dumps({
        "user_id": chosen_user_id,
        "duration": chosen_duration_value
    })
)

print(response)
