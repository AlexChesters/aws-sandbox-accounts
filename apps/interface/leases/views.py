from django.http import HttpResponse
import boto3

from leases.utils.deserialise import deserialise

sandbox_admin_session = boto3.Session(profile_name="sandbox-administrator")
dynamo = sandbox_admin_session.client("dynamodb")

def index(request):
    active_leases_response = dynamo.query(
        TableName="test-aws-sandbox-accounts-account-pool",
        KeyConditionExpression="pk = :pk_val",
        ExpressionAttributeValues={":pk_val": {"S": "lease_status#active"}}
    )

    active_leases = deserialise(active_leases_response)

    print(active_leases)

    return HttpResponse("Hello, world!")
