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

    def _deserialise_one(self, account: dict):
        return {k: self.deserializer.deserialize(v) for k,v in account.items()}

    def _deserialise_many(self, accounts: list[dict]):
        accounts = [self._deserialise_one(account) for account in accounts]

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

        return self._deserialise_many(result["Items"])

    def remove_account(self, account_id: str):
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

    def add_account(self, account_id: str):
        self.dynamo.put_item(
            TableName=self.table_name,
            Item={
                "pk": {
                    "S": "account"
                },
                "sk": {
                    "S": account_id
                },
                "status": {
                    "S": "dirty"
                }
            }
        )
