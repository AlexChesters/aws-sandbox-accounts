import boto3
import inquirer

from lease_manager.leases.create import create_lease
from lease_manager.leases.list_active import list_active_leases
from lease_manager.leases.invalidate import invalidate_lease
from lease_manager.identities.user_details import get_user_details
from lease_manager.utils.flatten import flatten

management_session = boto3.Session(profile_name="management")
identity_store = management_session.client("identitystore")

list_group_memberships_paginator = identity_store.get_paginator("list_group_memberships")

results = list_group_memberships_paginator.paginate(
    IdentityStoreId="d-93677ee9b2",
    GroupId="a24534e4-5021-7007-5383-41bcc820f470"
)
flat_results = flatten(result["GroupMemberships"] for result in results)

users = []

for member in flat_results:
    user_details = get_user_details(member["MemberId"]["UserId"])
    users.append((user_details["UserName"], user_details["UserId"]))

initial_answers = inquirer.prompt([
    inquirer.List(
        "action",
        message="What do you want to do?",
        choices=[
            ("Create a lease", "create"),
            ("Invalidate a lease", "invalidate"),
            ("List active leases", "list")
        ]
    )
])

match initial_answers["action"]:
    case "create":
        durations = [
            ("5 minutes", "5m"),
            ("30 minutes", "30m"),
            ("1 hour", "1h"),
            ("3 hours", "3h"),
            ("6 hours", "6h"),
            ("12 hours", "12h"),
            ("24 hours", "24h"),
            ("3 days", "3d"),
            ("7 days", "7d")
        ]

        create_answers = inquirer.prompt([
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

        chosen_user_display_name, chosen_user_id = next(user for user in users if user[1] == create_answers["user"])
        chosen_duration_display, chosen_duration_value = next(duration for duration in durations if duration[1] == create_answers["duration"])

        create_lease(chosen_user_id, chosen_user_display_name, chosen_duration_value)
    case "invalidate":
        invalidate_answers = inquirer.prompt([
            inquirer.Text(
                "lease_id",
                message="Which lease do you want to invalidate?"
            )
        ])

        invalidate_lease(invalidate_answers["lease_id"])
    case "list":
        list_active_leases()
