from enum import Enum

from pydantic import BaseModel

class AccountStatus(str, Enum):
    AVAILABLE = "AVAILABLE"
    LEASED = "LEASED"
    DIRTY = "DIRTY"
    FAILED = "FAILED"

class Account(BaseModel):
    account_id: str
    status: AccountStatus

    def to_json(self):
        return {
            "account_id": self.account_id,
            "status": self.status.value
        }
