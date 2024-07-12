from aws_lambda_powertools import Logger

logger = Logger()

def create_lease(event, sso_client):
    response = sso_client.create_account_assignment(
        InstanceArn="arn:aws:sso:::instance/ssoins-680483867be3e0a4",
        PermissionSetArn="arn:aws:sso:::permissionSet/ssoins-680483867be3e0a4/ps-2fe74c0708584223",
        PrincipalId=event["user_id"],
        PrincipalType="USER",
        TargetId=event["account"]["account_id"],
        TargetType="AWS_ACCOUNT"
    )

    logger.info(response)
