import argparse

import boto3

from db_seeder.utils.serialiser import serialise

parser = argparse.ArgumentParser()
parser.add_argument("--table-name", required=True)
args = parser.parse_args()

session = boto3.Session(profile_name="sandbox-administrator")
dynamodb = session.client("dynamodb")
table_name = args.table_name

response = dynamodb.scan(
    TableName=table_name,
    FilterExpression="begins_with(pk, :prefix)",
    ExpressionAttributeValues={
        ":prefix": {"S": "lease_id#"}
    },
    ProjectionExpression="pk"
)

for item in response["Items"]:
    dynamodb.delete_item(
        TableName=table_name,
        Key={"pk": item["pk"]}
    )

dynamodb.transact_write_items(
        TransactItems=[
            {
                "Put": {
                    "TableName": table_name,
                    "Item": serialise({
                        "pk": "account_status#all",
                        "data": ["905418121097"]
                    })
                }
            },
            {
                "Put": {
                    "TableName": table_name,
                    "Item": serialise({
                        "pk": "account_status#available",
                        "data": []
                    })
                }
            },
            {
                "Put": {
                    "TableName": table_name,
                    "Item": serialise({
                        "pk": "account_status#leased",
                        "data": []
                    })
                }
            },
            {
                "Put": {
                    "TableName": table_name,
                    "Item": serialise({
                        "pk": "account_status#dirty",
                        "data": ["905418121097"]
                    })
                }
            },
            {
                "Put": {
                    "TableName": table_name,
                    "Item": serialise({
                        "pk": "account_status#failed",
                        "data": []
                    })
                }
            },
            {
                "Put": {
                    "TableName": table_name,
                    "Item": serialise({
                        "pk": "lease_status#active",
                        "data": []
                    })
                }
            }
        ]
    )
