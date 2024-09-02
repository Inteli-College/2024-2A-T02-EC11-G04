from typing import List, Optional

from utils import SessionManager
from models import Token
from schemas import TokenInput, TokenOutput


class AuthRepository:
    def __init__(self, session: SessionManager):
        self._managed_session = session
    
    def create_token(self, data: TokenInput) -> Optional[TokenOutput]:
        with self._managed_session as session:
            token = Token(**data.model_dump())
            session.add(token)
            session.commit()
            session.refresh(token)
            return TokenOutput(token_id=token.id, token=token.token,
                            expiration=token.expiration,
                            revoked_token=token.revoked_token)

    def get_all_tokens(self) -> List[Optional[TokenOutput]]:
        pass

    def get_token_by_id(self, token_id: int) -> Optional[TokenOutput]:
        pass

    def get_all_tokens_by_user_id(self, user_id: int) -> List[Optional[TokenOutput]]:
        pass

    def revoke(self, token_id: int) -> bool:
        pass

    def delete_token_by_id(self, token_id: int) -> None:
        pass

    def delete_all_tokens_by_user_id(self, user_id: int) -> None:
        pass

