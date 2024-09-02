from pydantic import BaseModel

from typing import Optional


class UserInput(BaseModel):
    username: str
    email: Optional[str]


class UserOutput(BaseModel):
    user_id: int
    username: str
    email: Optional[str]
    created_at: str

