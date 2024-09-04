from config import engine
from models.token import Token
from models.user import User


def create_tables() -> None:
    """Function to create tables in the database.
    """
    Token.metadata.create_all(bind=engine)
    User.metadata.create_all(bind=engine)
