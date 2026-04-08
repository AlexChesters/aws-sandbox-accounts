import boto3

_identity_store = None
_dynamo = None
_step_functions = None


def identity_store():
    global _identity_store
    if _identity_store is None:
        session = boto3.Session(profile_name="management", region_name="eu-west-1")
        _identity_store = session.client("identitystore")
    return _identity_store


def dynamo():
    global _dynamo
    if _dynamo is None:
        session = boto3.Session(profile_name="sandbox-administrator", region_name="eu-west-1")
        _dynamo = session.client("dynamodb")
    return _dynamo


def step_functions():
    global _step_functions
    if _step_functions is None:
        session = boto3.Session(profile_name="sandbox-administrator", region_name="eu-west-1")
        _step_functions = session.client("stepfunctions")
    return _step_functions
