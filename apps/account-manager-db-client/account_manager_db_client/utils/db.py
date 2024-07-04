from boto3.dynamodb.types import TypeSerializer

serialiser = TypeSerializer()

def serialise(i):
    if isinstance(i, dict):
        return {k: serialiser.serialize(v) for k,v in i.items()}
    elif isinstance(i, list):
        return [serialiser.serialize(v) for v in i]
