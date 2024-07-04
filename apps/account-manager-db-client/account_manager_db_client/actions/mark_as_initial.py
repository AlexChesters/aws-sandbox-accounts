from account_manager_db_client.utils.db import serialise

def mark_as_initial(event, dynamo_client, table_name):
    account_id = event.get("params", {}).get("account_id")

    if not account_id:
        raise ValueError("'params.account_id' not provided in event")

    dynamo_client.transact_write_items(
        TransactItems=[
            {
                "Put": {
                    "TableName": table_name,
                    "Item": serialise({
                        "pk": "account_id#905418121097",
                        "data": "initial"
                    })
                }
            },
            {
                "Update": {
                    "TableName": table_name,
                    "Item": serialise({
                        "pk": "account_status#all"
                    }),
                    "UpdateExpression": "SET #data = list_append(#data, :values)",
                    "ExpressionAttributeNames": {
                        "#data": "data"
                    },
                    "ExpressionAttributeValues": {
                        ":values": serialise(["905418121097"])
                    }
                }
            },
            {
                "Update": {
                    "TableName": table_name,
                    "Item": serialise({
                        "pk": "account_status#initial",
                    }),
                    "UpdateExpression": "SET #data = list_append(#data, :values)",
                    "ExpressionAttributeNames": {
                        "#data": "data"
                    },
                    "ExpressionAttributeValues": {
                        ":values": serialise(["905418121097"])
                    }
                }
            }
        ]
    )
