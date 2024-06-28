import boto3

class DBClient:
    def __init__(self):
        session = boto3.Session(profile_name="sandbox-administrator")
        self.dynamo = session.client("dynamodb")

    def list_accounts(self, table_name):
        result = self.dynamo.query(
            TableName=table_name,
            KeyConditionExpression="pk = :pk",
            ExpressionAttributeValues={
                ":pk": {
                    "S": "account"
                }
            }
        )

        return result["Items"]

    def remove_account(self, account_id):
        pass
