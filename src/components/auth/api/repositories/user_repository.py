from typing import List, Optional

from utils import SessionManager


class UserRepository:
    def __init__(self, session: SessionManager):
        self.session = session
    
    def create_user(self, data: dict) -> dict:
        pass

    def get_user_by_id(self, user_id: int) -> Optional[dict]:
        pass

    def get_all_users(self) -> List[Optional[dict]]:
        pass

    def update_user(self, user_id: int, data: dict) -> dict:
        pass

    def delete_user(self, user_id: int) -> None:
        pass
