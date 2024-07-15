import boto3
import inquirer

from lease_manager.utils.flatten import flatten

management_session = boto3.Session(profile_name="management")
identity_store = management_session.client("identitystore")
list_users_paginator = identity_store.get_paginator("list_users")

results = list_users_paginator.paginate(IdentityStoreId="d-93677ee9b2")
flat_results = flatten(result["Users"] for result in results)
users = [(user["UserName"], user["UserId"]) for user in flat_results]

answers = inquirer.prompt([
    inquirer.List(
        "user",
        message="Which user do you want to create a lease for?",
        choices=users
    )
])

chosen_user = next(user for user in users if user[1] == answers["user"])
print(chosen_user)
