from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from config import engine

from .logger import Logger

_logger = Logger(logger_name=__name__)._get_logger()


class SessionManager:
    def __init__(self):
        self.session = None

    def __enter__(self):
        """Represents the start of the session.

        Returns:
            self: Returns the session object.
        """
        self.session = Session(bind=engine)
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Represents the end of the session.

        Args:
            exc_type (ExceptionType): Exception type.
            exc_val (ExceptionValue): Exception value.
            exc_tb (ExceptionTraceback): Exception traceback.

        Raises:
            e.with_traceback: SQLAlchemyError with traceback.

        Returns:
            bool: Clean up the session and return False.
        """
        try:
            if exc_type is not None:
                _logger.error(
                    "Transaction rolled back due to exception: %s",
                    exc_val
                )
                self.session.rollback()
            else:
                self.session.commit()
        except SQLAlchemyError as e:
            _logger.error(
                "SQLAlchemy Error during transaction | Error: %s",
                str(e)
            )
            raise e.with_traceback(exc_tb)
        finally:
            self.session.close()
            self.session = None

        return False

    def __call__(self):
        if self.session is None:
            raise RuntimeError("SessionManager must be implemented using with statements.")
        return self.session
