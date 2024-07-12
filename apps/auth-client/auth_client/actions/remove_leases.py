from aws_lambda_powertools import Logger

logger = Logger()

def remove_leases(event, sso_client):
    params = event["params"]

    for item in params["items"]:
        account_id = item["account_id"]
        user_id = item["user_id"]
        lease_id = item["lease_id"]

        response = sso_client.delete_account_assignment(
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
            "lease_id": lease_id
        }
