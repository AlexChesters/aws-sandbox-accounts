from boto3.dynamodb.types import TypeSerializer
from boto3.dynamodb.types import TypeDeserializer

serialiser = TypeSerializer()
deserialiser = TypeDeserializer()

def dynamo_to_python(dynamo_object: dict) -> dict:
    return {
        k: deserialiser.deserialize(v)
        for k, v in dynamo_object.items()
    }

def python_to_dynamo(python_object: dict) -> dict:
    return {
        k: serialiser.serialize(v)
        for k, v in python_object.items()
    }
