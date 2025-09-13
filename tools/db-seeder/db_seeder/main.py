import argparse

import boto3

from db_seeder.utils.serialiser import serialise

parser = argparse.ArgumentParser()
parser.add_argument("--env", required=True, choices=["test", "live"], help="The environment to seed the database for.")
args = parser.parse_args()

session = boto3.Session(profile_name="sandbox-administrator", region_name="eu-west-1")
dynamodb = session.client("dynamodb")

args_map = {
    "test": {
        "table_name": "test-aws-sandbox-accounts-account-pool",
        "accounts": ["227301199018"]
    },
    "live": {
        "table_name": "live-aws-sandbox-accounts-account-pool",
        "accounts": ["905418121097", "891377354273", "471112670300"]
    }
}
table_name = args_map[args.env]["table_name"]

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
                        "data": args_map[args.env]["accounts"]
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
                        "data": args_map[args.env]["accounts"]
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
                        "pk": "account_status#pending",
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
            },
            {
                "Put": {
                    "TableName": table_name,
                    "Item": serialise({
                        "pk": "lease_status#pending",
                        "data": []
                    })
                }
            }
        ]
    )
