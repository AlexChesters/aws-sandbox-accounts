from pydantic import BaseModel

class User(BaseModel):
    user_id: str
    user_name: str

    def to_json(self):
        return {
            "userId": self.user_id,
            "userName": self.user_name
        }
