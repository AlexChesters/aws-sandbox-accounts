import boto3

def list_accounts(table_name):
    session = boto3.Session(profile_name="sandbox-administrator")
    dynamo = session.client("dynamodb")

    result = dynamo.query(
        TableName=table_name,
        KeyConditionExpression="pk = :pk",
        ExpressionAttributeValues={
            ":pk": {
                "S": "account"
            }
        }
    )

    return result["Items"]
