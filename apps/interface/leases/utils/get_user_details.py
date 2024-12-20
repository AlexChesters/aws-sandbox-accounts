import boto3

management_session = boto3.Session(profile_name="management")
identity_store = management_session.client("identitystore")

def get_user_details(user_id: str):
    return identity_store.describe_user(
        IdentityStoreId="d-93677ee9b2",
        UserId=user_id
    )
