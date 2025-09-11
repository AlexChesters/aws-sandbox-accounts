from enum import Enum

from pydantic import BaseModel

class AccountStatus(str, Enum):
    AVAILABLE = "available"
    LEASED = "leased"
    DIRTY = "dirty"
    FAILED = "failed"

class Account(BaseModel):
    account_id: str
    status: AccountStatus

    def to_json(self):
        return {
            "account_id": self.account_id,
            "status": self.status.value
        }
