from account_manager_db_client.utils.db import dynamo_to_python, python_to_dynamo

class AccountStatus:
    def __init__(self, dynamo_data) -> None:
        deserialised_data = dynamo_to_python(dynamo_data)

        self._pk = deserialised_data["pk"]
        self.accounts = set(deserialised_data["data"])

    def to_dynamo(self):
        return python_to_dynamo({
            "pk": self._pk,
            "data": list(self.accounts)
        })
