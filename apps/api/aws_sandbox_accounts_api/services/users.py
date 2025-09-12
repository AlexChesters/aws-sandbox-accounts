import os

from aws_sandbox_accounts_api.models.user import User
from aws_sandbox_accounts_api.utils.assume_role import assume_role
from aws_sandbox_accounts_api.utils.flatten import flatten

MANAGEMENT_ACCOUNT_ROLE_ARN = os.environ["MANAGEMENT_ACCOUNT_ROLE_ARN"]

def get_all_users() -> list[User]:
    management_account_session = assume_role(role_arn=MANAGEMENT_ACCOUNT_ROLE_ARN)

    identity_store = management_account_session.client("identitystore")

    list_group_memberships_paginator = identity_store.get_paginator("list_group_memberships")

    results = list_group_memberships_paginator.paginate(
        IdentityStoreId="d-93677ee9b2",
        GroupId="a24534e4-5021-7007-5383-41bcc820f470"
    )
    flat_results = flatten(result["GroupMemberships"] for result in results)

    return flat_results
