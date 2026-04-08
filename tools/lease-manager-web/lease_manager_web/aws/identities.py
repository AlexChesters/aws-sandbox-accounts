import lease_manager_web.aws.sessions as sessions

IDENTITY_STORE_ID = "d-93677ee9b2"
GROUP_ID = "a24534e4-5021-7007-5383-41bcc820f470"


def list_users() -> list[tuple[str, str]]:
    client = sessions.identity_store()
    paginator = client.get_paginator("list_group_memberships")
    pages = paginator.paginate(IdentityStoreId=IDENTITY_STORE_ID, GroupId=GROUP_ID)

    users = []
    for page in pages:
        for member in page["GroupMemberships"]:
            user_id = member["MemberId"]["UserId"]
            response = client.describe_user(
                IdentityStoreId=IDENTITY_STORE_ID, UserId=user_id
            )
            users.append((response["UserName"], user_id))

    return users


def get_username(user_id: str) -> str:
    response = sessions.identity_store().describe_user(
        IdentityStoreId=IDENTITY_STORE_ID, UserId=user_id
    )
    return response["UserName"]
