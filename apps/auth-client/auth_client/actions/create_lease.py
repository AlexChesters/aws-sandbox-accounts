from datetime import datetime, timedelta

from aws_lambda_powertools import Logger

logger = Logger()

def create_lease(event, sso_client):
    params = event["params"]
    account_id = params["account"]["account_id"]
    user_id = params["user_id"]

    response = sso_client.create_account_assignment(
        InstanceArn="arn:aws:sso:::instance/ssoins-680483867be3e0a4",
        PermissionSetArn="arn:aws:sso:::permissionSet/ssoins-680483867be3e0a4/ps-2fe74c0708584223",
        PrincipalId=user_id,
        PrincipalType="USER",
        TargetId=account_id,
        TargetType="AWS_ACCOUNT"
    )

    logger.info(response)

    # low limit for testing
    fifteen_minutes_from_now = datetime.now() + timedelta(minutes=15)

    return {
        "account_id": account_id,
        "user_id": user_id,
        "expires": fifteen_minutes_from_now.isoformat()
    }
