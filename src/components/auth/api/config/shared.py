from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase

from .settings import enviroment_settings

connection_string = enviroment_settings.postgres_dsn.unicode_string()
engine = create_engine(
    url=connection_string,
    pool_size=10,
    max_overflow=15,
    pool_pre_ping=True,
    pool_recycle=3600
)


class Base(DeclarativeBase):
    pass

