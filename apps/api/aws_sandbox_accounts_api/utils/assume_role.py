import os

import boto3

function_name = os.environ["AWS_LAMBDA_FUNCTION_NAME"]

def assume_role(*, role_arn: str) -> boto3.Session:
    sts = boto3.client("sts")
    assumed_role_object = sts.assume_role(
        RoleArn=role_arn,
        RoleSessionName=function_name
    )

    credentials = assumed_role_object["Credentials"]

    return boto3.Session(
        aws_access_key_id=credentials["AccessKeyId"],
        aws_secret_access_key=credentials["SecretAccessKey"],
        aws_session_token=credentials["SessionToken"]
    )
