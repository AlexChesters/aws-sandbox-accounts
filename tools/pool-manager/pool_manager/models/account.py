import json

class Account:
    def __init__(self, account_id: str, status: str):
        self.account_id = account_id
        self.status = status

    def to_dict(self):
        return {
            "account_id": self.account_id,
            "status": self.status
        }

    def __str__(self):
        return json.dumps(self.to_dict())
