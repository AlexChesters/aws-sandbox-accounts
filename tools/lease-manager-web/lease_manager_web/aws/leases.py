from datetime import datetime, timedelta, timezone

from boto3.dynamodb.types import TypeDeserializer, TypeSerializer

import lease_manager_web.aws.sessions as sessions

TABLE_NAME = "live-aws-sandbox-accounts-account-pool"

_deserializer = TypeDeserializer()
_serializer = TypeSerializer()


def _deserialise(response: dict) -> dict:
    return [{k: _deserializer.deserialize(v) for k, v in item.items()} for item in response["Items"]][0]


def _serialise(item: dict) -> dict:
    return {k: _serializer.serialize(v) for k, v in item.items()}


def list_active_leases() -> dict[str, dict]:
    db = sessions.dynamo()
    active_response = db.query(
        TableName=TABLE_NAME,
        KeyConditionExpression="pk = :pk_val",
        ExpressionAttributeValues={":pk_val": {"S": "lease_status#active"}},
    )
    active = _deserialise(active_response)

    leases = {}
    for lease_id in active["data"]:
        lease_response = db.query(
            TableName=TABLE_NAME,
            KeyConditionExpression="pk = :pk_val",
            ExpressionAttributeValues={":pk_val": {"S": f"lease_id#{lease_id}"}},
        )
        leases[lease_id] = _deserialise(lease_response)["data"]

    return leases


def get_lease(lease_id: str) -> dict:
    response = sessions.dynamo().query(
        TableName=TABLE_NAME,
        KeyConditionExpression="pk = :pk_val",
        ExpressionAttributeValues={":pk_val": {"S": f"lease_id#{lease_id}"}},
    )
    return _deserialise(response)


def expire_lease(lease_id: str, lease_data: dict) -> None:
    lease_data["expires"] = (datetime.now(timezone.utc) - timedelta(hours=1)).strftime(
        "%Y-%m-%dT%H:%M:%S.%f"
    )[:-3]

    sessions.dynamo().put_item(
        TableName=TABLE_NAME,
        Item={
            "pk": {"S": f"lease_id#{lease_id}"},
            "data": {"M": _serialise(lease_data)},
        },
    )
