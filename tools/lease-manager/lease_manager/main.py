import json
import time
import sys

import boto3
import inquirer

from lease_manager.utils.flatten import flatten

management_session = boto3.Session(profile_name="management")
sandbox_admin_session = boto3.Session(profile_name="sandbox-administrator")

identity_store = management_session.client("identitystore")
step_functions = sandbox_admin_session.client("stepfunctions")

list_group_memberships_paginator = identity_store.get_paginator("list_group_memberships")

results = list_group_memberships_paginator.paginate(
    IdentityStoreId="d-93677ee9b2",
    GroupId="a24534e4-5021-7007-5383-41bcc820f470"
)
flat_results = flatten(result["GroupMemberships"] for result in results)

users = []

for member in flat_results:
    user_details = identity_store.describe_user(
        IdentityStoreId="d-93677ee9b2",
        UserId=member["MemberId"]["UserId"]
    )
    users.append((user_details["UserName"], user_details["UserId"]))

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

start_response = step_functions.start_execution(
    # TODO: use live when it is ready
    stateMachineArn="arn:aws:states:eu-west-1:654654632738:stateMachine:test-aws-sandbox-accounts-lease-creator",
    input=json.dumps({
        "user_id": chosen_user_id,
        "duration": chosen_duration_value
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
            print(f"[SUCCESS] - lease successfully created for {chosen_user_display_name}")
            sys.exit(0)
        case _:
            print(f"[ERROR] - error creating lease: {status}")
            sys.exit(1)

    time.sleep(10)
