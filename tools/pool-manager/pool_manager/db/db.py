import boto3

class DBClient:
    def __init__(self):
        session = boto3.Session(profile_name="sandbox-administrator")
        self.dynamo = session.client("dynamodb")
        self.table_name = "test-aws-sandbox-accounts-account-pool"

    def list_accounts(self):
        result = self.dynamo.query(
            TableName=self.table_name,
            KeyConditionExpression="pk = :pk",
            ExpressionAttributeValues={
                ":pk": {
                    "S": "account"
                }
            }
        )

        return result["Items"]

    def remove_account(self, account_id):
        self.dynamo.delete_item(
            TableName=self.table_name,
            Key={
                "pk": {
                    "S": account_id
                }
            }
        )
