from datetime import datetime, timedelta

from aws_lambda_powertools import Logger

logger = Logger()

# map of duration string: minutes
valid_durations = {
    "5m": 5,
    "30m": 30,
    "1h": 60,
    "3h": 180,
    "6h": 360,
    "12h": 720,
    "24h": 1440
}

def create_lease(event, sso_client):
    params = event["params"]
    account_id = params["account"]["account_id"]
    user_id = params["user_id"]
    duration_param = params["duration"]

    duration = valid_durations.get(duration_param, None)

    if not duration:
        raise ValueError(f"{duration_param} is not a valid duration, valid durations: {valid_durations.keys()}")

    response = sso_client.create_account_assignment(
        InstanceArn="arn:aws:sso:::instance/ssoins-680483867be3e0a4",
        PermissionSetArn="arn:aws:sso:::permissionSet/ssoins-680483867be3e0a4/ps-2fe74c0708584223",
        PrincipalId=user_id,
        PrincipalType="USER",
        TargetId=account_id,
        TargetType="AWS_ACCOUNT"
    )

    logger.info(response)

    return {
        "account_id": account_id,
        "user_id": user_id,
        "expires": datetime.now() + timedelta(minutes=duration).isoformat()
    }
