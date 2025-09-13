from enum import Enum

from pydantic import BaseModel

class AccountStatus(str, Enum):
    AVAILABLE = "available"
    PENDING = "pending"
    LEASED = "leased"
    DIRTY = "dirty"
    FAILED = "failed"

class Account(BaseModel):
    account_id: str
    name: str
    status: AccountStatus

    def to_json(self):
        return {
            "account_id": self.account_id,
            "name": self.name,
            "status": self.status.value
        }
