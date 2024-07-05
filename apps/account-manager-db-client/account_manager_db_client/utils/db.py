from boto3.dynamodb.types import TypeSerializer
from boto3.dynamodb.types import TypeDeserializer

serialiser = TypeSerializer()
deserialiser = TypeDeserializer()

def serialise(i):
    if isinstance(i, dict):
        return {k: serialiser.serialize(v) for k,v in i.items()}
    elif isinstance(i, list):
        return [serialiser.serialize(v) for v in i]

def deserialise(i):
    if isinstance(i, dict):
        return {k: deserialiser.deserialize(v) for k,v in i.items()}
    elif isinstance(i, list):
        return [
            {k: deserialiser.deserialize(v) for k,v in v.items()} if isinstance(v, dict) else deserialiser.deserialize(v)
            for v in i
        ]
