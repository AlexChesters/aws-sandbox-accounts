from boto3.dynamodb.types import TypeDeserializer

deserializer = TypeDeserializer()

def deserialise(response):
    return [{k: deserializer.deserialize(v) for k, v in item.items()} for item in response["Items"]][0]
