import json
from datetime import datetime

from db_client.utils.db import dynamo_to_python, python_to_dynamo

class Lease:
    def __init__(self, dynamo_data) -> None:
        deserialised_data = dynamo_to_python(dynamo_data)

        self.lease_id = deserialised_data["pk"].split("#")[1]
        self.expires = datetime.fromisoformat(deserialised_data["data"]["expires"])
        self.state = deserialised_data["data"]["state"]
        self.user = deserialised_data["data"]["user"]
        self.account = deserialised_data["data"]["account"]

    def __str__(self) -> str:
        return json.dumps(self.to_dynamo())

    def to_dynamo(self) -> dict:
        return python_to_dynamo({
            "pk": f"lease_id#{self.lease_id}",
            "data": {
                "expires": self.expires.isoformat(),
                "state": self.state,
                "user": self.user,
                "account": self.account
            }
        })
