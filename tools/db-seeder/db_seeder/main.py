import argparse

import boto3

from db_seeder.utils.serialiser import serialise

parser = argparse.ArgumentParser()
parser.add_argument("--table-name", required=True)
args = parser.parse_args()

session = boto3.Session(profile_name="sandbox-administrator")
dynamodb = session.client("dynamodb")
table_name = args.table_name

dynamodb.transact_write_items(
        TransactItems=[
            {
                "Update": {
                    "TableName": table_name,
                    "Key": serialise({
                        "pk": "account_status#all"
                    }),
                    "UpdateExpression": "SET #data = :empty_list",
                    "ExpressionAttributeNames": {
                        "#data": "data"
                    },
                    "ExpressionAttributeValues": serialise({
                        ":empty_list": []
                    })
                }
            },
            {
                "Update": {
                    "TableName": table_name,
                    "Key": serialise({
                        "pk": "account_status#available"
                    }),
                    "UpdateExpression": "SET #data = :empty_list",
                    "ExpressionAttributeNames": {
                        "#data": "data"
                    },
                    "ExpressionAttributeValues": serialise({
                        ":empty_list": []
                    })
                }
            },
            {
                "Update": {
                    "TableName": table_name,
                    "Key": serialise({
                        "pk": "account_status#leased"
                    }),
                    "UpdateExpression": "SET #data = :empty_list",
                    "ExpressionAttributeNames": {
                        "#data": "data"
                    },
                    "ExpressionAttributeValues": serialise({
                        ":empty_list": []
                    })
                }
            },
            {
                "Update": {
                    "TableName": table_name,
                    "Key": serialise({
                        "pk": "account_status#initial"
                    }),
                    "UpdateExpression": "SET #data = :empty_list",
                    "ExpressionAttributeNames": {
                        "#data": "data"
                    },
                    "ExpressionAttributeValues": serialise({
                        ":empty_list": []
                    })
                }
            }
        ]
    )
