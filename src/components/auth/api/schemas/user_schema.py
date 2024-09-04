from pydantic import BaseModel

from datetime import datetime
from typing import Annotated, List, Optional

from .token_schema import TokenOutput

class UserInput(BaseModel):
    username: str
    email: Optional[str]


class UserOutput(BaseModel):
    username: Annotated[str, "Username"]
    email: Annotated[Optional[str], "Email"]
    tokens: Annotated[List[Optional[TokenOutput]], "Associated tokens"]
    created_at: Annotated[datetime, "Creation date"]

