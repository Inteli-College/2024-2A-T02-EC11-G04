from pydantic import BaseModel, computed_field

from datetime import datetime
from typing import Annotated, List
from uuid import uuid4

from utils import TokenEncoder

_encoder = TokenEncoder()


class TokenInput(BaseModel):
    user_id: Annotated[int, "User ID"]
    expiration: Annotated[datetime, "Expiration date"]

    @computed_field
    @property
    def token(self) -> str:
        return _encoder(self.user_id, uuid4().hex, self.expiration)


class TokenOutput(BaseModel):
    token_id: Annotated[int, "Token ID"]
    token: Annotated[str, "Token"]
    expiration: Annotated[datetime, "Expiration date"]
    revoked_token: Annotated[bool, "Revoked token"]
