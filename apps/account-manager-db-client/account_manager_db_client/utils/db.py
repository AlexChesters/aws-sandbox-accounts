from boto3.dynamodb.types import TypeSerializer

serialiser = TypeSerializer()

def serialise(obj):
    return {k: serialiser.serialize(v) for k,v in obj.items()}
