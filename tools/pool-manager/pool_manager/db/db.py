import boto3
from boto3.dynamodb.types import TypeDeserializer, TypeSerializer

from pool_manager.utils.logger import Logger
from pool_manager.models.account import Account

class DBClient:
    def __init__(self):
        session = boto3.Session(profile_name="sandbox-administrator")
        self.dynamo = session.client("dynamodb")
        self.table_name = "test-aws-sandbox-accounts-account-pool"
        self.deserializer = TypeDeserializer()
        self.serializer = TypeSerializer()
        self.logger = Logger()

    def _deserialise(self, accounts):
        accounts = [{k: self.deserializer.deserialize(v) for k,v in item.items()} for item in accounts]

        return [Account(account["sk"], account["status"]) for account in accounts]

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

        return self._deserialise(result["Items"])

    def remove_account(self, account_id):
        self.dynamo.delete_item(
            TableName=self.table_name,
            Key={
                "pk": {
                    "S": "account"
                },
                "sk": {
                    "S": account_id
                }
            }
        )
