import os

import boto3
from boto3.dynamodb.types import TypeSerializer, TypeDeserializer

serializer = TypeSerializer()
deserializer = TypeDeserializer()

def __get_session() -> boto3.Session:
    if os.environ.get("AWS_LAMBDA_FUNCTION_NAME"):
        return boto3.Session()
    else:
        return boto3.Session(profile_name="sandbox-administrator")

def get_client(client_name: str) -> boto3.client:
    return __get_session().client(client_name, region_name=os.environ.get("AWS_REGION", "eu-west-1"))

def __get_table_name() -> str:
    return os.environ.get("TABLE_NAME", "live-aws-sandbox-accounts-account-pool")

def get_item(*, pk: str):
    table_name = __get_table_name()
    response = get_client("dynamodb").get_item(
        TableName=table_name,
        Key={"pk": serializer.serialize(pk)}
    )
    item = response.get("Item")

    if item is None:
        return None

    return { k: deserializer.deserialize(v) for k, v in item.items() }
