from time import monotonic, sleep

from aws_lambda_powertools import Logger

logger = Logger()

INSTANCE_ARN = "arn:aws:sso:::instance/ssoins-680483867be3e0a4"
PERMISSION_SET_ARN = (
    "arn:aws:sso:::permissionSet/"
    "ssoins-680483867be3e0a4/ps-2fe74c0708584223"
)
DELETION_TIMEOUT_SECONDS = 90
POLL_INTERVAL_SECONDS = 1


def remove_leases(event, sso_client):
    params = event["params"]
    deletions = []
    pending_deletions = {}

    for item in params["items"]:
        account_id = item["account_id"]
        user_id = item["user_id"]
        lease_id = item["lease_id"]

        response = sso_client.delete_account_assignment(
            InstanceArn=INSTANCE_ARN,
            PermissionSetArn=PERMISSION_SET_ARN,
            PrincipalId=user_id,
            PrincipalType="USER",
            TargetId=account_id,
            TargetType="AWS_ACCOUNT"
        )

        logger.info(response)

        deletion_status = response["AccountAssignmentDeletionStatus"]
        if deletion_status["Status"] == "FAILED":
            failure_reason = deletion_status.get("FailureReason", "unknown reason")
            raise RuntimeError(
                f"Identity Center assignment deletion failed for lease "
                f"{lease_id}: {failure_reason}"
            )

        if deletion_status["Status"] not in {"IN_PROGRESS", "SUCCEEDED"}:
            raise RuntimeError(
                "Identity Center returned an unexpected assignment deletion "
                f"status: {deletion_status['Status']!r}"
            )

        deletion = {
            "account_id": account_id,
            "lease_id": lease_id,
            "request_id": deletion_status["RequestId"],
        }
        deletions.append(deletion)
        pending_deletions[deletion["request_id"]] = deletion

    deadline = monotonic() + DELETION_TIMEOUT_SECONDS

    while pending_deletions:
        for request_id in tuple(pending_deletions):
            response = sso_client.describe_account_assignment_deletion_status(
                AccountAssignmentDeletionRequestId=request_id,
                InstanceArn=INSTANCE_ARN,
            )
            logger.info(response)

            deletion_status = response["AccountAssignmentDeletionStatus"]
            status = deletion_status["Status"]

            if status == "SUCCEEDED":
                del pending_deletions[request_id]
            elif status == "FAILED":
                deletion = pending_deletions[request_id]
                failure_reason = deletion_status.get(
                    "FailureReason",
                    "unknown reason",
                )
                raise RuntimeError(
                    f"Identity Center assignment deletion failed for lease "
                    f"{deletion['lease_id']}: {failure_reason}"
                )
            elif status != "IN_PROGRESS":
                raise RuntimeError(
                    "Identity Center returned an unexpected assignment deletion "
                    f"status: {status!r}"
                )

        if pending_deletions:
            if monotonic() >= deadline:
                pending_lease_ids = [
                    deletion["lease_id"]
                    for deletion in pending_deletions.values()
                ]
                raise TimeoutError(
                    "Timed out waiting for Identity Center assignment deletions "
                    f"for leases: {pending_lease_ids}"
                )
            sleep(POLL_INTERVAL_SECONDS)

    return deletions
