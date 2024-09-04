from typing import List, Optional

from utils import Logger, SessionManager
from models import Token
from schemas import TokenInput, TokenOutput

_logger = Logger(logger_name=__name__)._get_logger()

class AuthRepository:
    def __init__(self, session: SessionManager):
        self._managed_session = session
    
    def create_token(self, data: TokenInput) -> Optional[TokenOutput]:
        try:
            with self._managed_session as session:
                token = Token(**data.model_dump())
                session.add(token)
                session.commit()
                session.refresh(token)
                return TokenOutput(token_id=token.id, token=token.token,
                                expiration=token.expiration,
                                revoked_token=token.revoked_token)
        except Exception as e:
            _logger.error("Error caught on token creation: %s", str(e))
            return None

    def get_token_by_id(self, token_id: int) -> Optional[TokenOutput]:
        with self._managed_session as session:
            token = session.query(Token).filter(Token.id == token_id).first()
            if token:
                return TokenOutput(token_id=token.id, token=token.token,
                                expiration=token.expiration,
                                revoked_token=token.revoked_token)
            _logger.info("Token not found")
            return None

    def get_all_tokens_by_user_id(self, user_id: int) -> List[Optional[TokenOutput]]:
        with self._managed_session as session:
            tokens = session.query(Token).filter(Token.user_id == user_id).all()
            return [TokenOutput(token_id=token.id, token=token.token,
                                expiration=token.expiration,
                                revoked_token=token.revoked_token) for token in tokens]

    def revoke_token(self, token_id: int) -> bool:
        with self._managed_session as session:
            token = session.query(Token).filter(Token.id == token_id).first()
            if token:
                token.revoked_token = True
                session.commit()
                return True
            return False

    def delete_token_by_id(self, token_id: int) -> None:
        with self._managed_session as session:
            token = session.query(Token).filter(Token.id == token_id).first()
            if token:
                session.delete(token)
                session.commit()

    def delete_all_tokens_by_user_id(self, user_id: int) -> None:
        with self._managed_session as session:
            tokens = session.query(Token).filter(Token.user_id == user_id).all()
            for token in tokens:
                session.delete(token)
            session.commit()
