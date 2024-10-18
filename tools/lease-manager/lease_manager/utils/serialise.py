from boto3.dynamodb.types import TypeSerializer

serializer = TypeSerializer()

def serialise(item):
    return {k: serializer.serialize(v) for k, v in item.items()}
