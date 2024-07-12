from datetime import datetime, timedelta

from aws_lambda_powertools import Logger

logger = Logger()

def create_lease(event, sso_client):
    account_id = event["account"]["account_id"]
    user_id = event["user_id"]

    response = sso_client.create_account_assignment(
        InstanceArn="arn:aws:sso:::instance/ssoins-680483867be3e0a4",
        PermissionSetArn="arn:aws:sso:::permissionSet/ssoins-680483867be3e0a4/ps-2fe74c0708584223",
        PrincipalId=user_id,
        PrincipalType="USER",
        TargetId=account_id,
        TargetType="AWS_ACCOUNT"
    )

    logger.info(response)

    two_hours_from_now = datetime.now() + timedelta(hours=2)

    return {
        "account_id": account_id,
        "user_id": user_id,
        "expires": two_hours_from_now.isoformat()
    }
