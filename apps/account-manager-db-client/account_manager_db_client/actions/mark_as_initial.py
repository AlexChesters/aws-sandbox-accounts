from aws_lambda_powertools import Logger

from account_manager_db_client.utils.db import serialise, deserialise

logger = Logger()

def mark_as_initial(event, dynamo_client, table_name):
    account_id = event.get("params", {}).get("account_id")

    if not account_id:
        raise ValueError("'params.account_id' not provided in event")

    # TODO: don't just blindly append to lists, because the same account ID will be in there multiple times
    # instead we may need to
    # 1. fetch all lists that we need too
    # 2. set them all to be the correct values
    # 3. write all lists back to the db

    get_items_response = dynamo_client.batch_get_item(
        RequestItems={
            table_name: {
                "Keys": [
                    serialise({ "pk": "account_status#all" }),
                    serialise({ "pk": "account_status#available" }),
                    serialise({ "pk": "account_status#leased" }),
                    serialise({ "pk": "account_status#initial" })
                ]
            }
        }
    )

    existing_data = deserialise(get_items_response["Responses"][table_name])

    all_accounts = next(item for item in existing_data if item["pk"] == "account_status#all")
    available_accounts = next(item for item in existing_data if item["pk"] == "account_status#available")
    leased_accounts = next(item for item in existing_data if item["pk"] == "account_status#leased")
    initial_accounts = next(item for item in existing_data if item["pk"] == "account_status#initial")

    logger.info(all_accounts)
    logger.info(available_accounts)
    logger.info(leased_accounts)
    logger.info(initial_accounts)

    # dynamo_client.transact_write_items(
    #     TransactItems=[
    #         {
    #             "Put": {
    #                 "TableName": table_name,
    #                 "Item": serialise({
    #                     "pk": "account_id#905418121097",
    #                     "data": "initial"
    #                 })
    #             }
    #         },
    #         {
    #             "Update": {
    #                 "TableName": table_name,
    #                 "Key": serialise({
    #                     "pk": "account_status#all"
    #                 }),
    #                 "UpdateExpression": "SET #data = list_append(#data, :values)",
    #                 "ExpressionAttributeNames": {
    #                     "#data": "data"
    #                 },
    #                 "ExpressionAttributeValues": serialise({
    #                     ":values": ["905418121097"]
    #                 })
    #             }
    #         },
    #         {
    #             "Update": {
    #                 "TableName": table_name,
    #                 "Key": serialise({
    #                     "pk": "account_status#initial",
    #                 }),
    #                 "UpdateExpression": "SET #data = list_append(#data, :values)",
    #                 "ExpressionAttributeNames": {
    #                     "#data": "data"
    #                 },
    #                 "ExpressionAttributeValues": serialise({
    #                     ":values": ["905418121097"]
    #                 })
    #             }
    #         }
    #     ]
    # )
