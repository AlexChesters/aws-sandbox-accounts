import json

from db_client.utils.db import dynamo_to_python, python_to_dynamo

class LeaseStatus:
    def __init__(self, dynamo_data) -> None:
        deserialised_data = dynamo_to_python(dynamo_data)

        self._pk = deserialised_data["pk"]
        self.leases = set(deserialised_data["data"])

    def __str__(self) -> str:
        return json.dumps(self.to_dynamo())

    def to_dynamo(self):
        return python_to_dynamo({
            "pk": self._pk,
            "data": list(self.leases)
        })
