from utils import SessionManager
from repositories import AuthRepository
from schemas import TokenInput, TokenOutput

class AuthService:
    def __init__(self, session: SessionManager):
        self.repository = AuthRepository(session)

    def create_token(self, data: TokenInput) -> TokenOutput:
        return self.repository.create_token(data)

    def get_all_tokens(self) -> list:
        return self.repository.get_all_tokens()

    def get_token_by_id(self, token_id: int) -> dict:
        return self.repository.get_token_by_id(token_id)

    def get_all_tokens_by_user_id(self, user_id: int) -> list:
        return self.repository.get_all_tokens_by_user_id(user_id)

    def revoke(self, token_id: int) -> bool:
        return self.repository.revoke(token_id)

    def delete_token_by_id(self, token_id: int) -> None:
        return self.repository.delete_token_by_id(token_id)

    def delete_all_tokens_by_user_id(self, user_id: int) -> None:
        return self.repository.delete_all_tokens_by_user_id(user_id)