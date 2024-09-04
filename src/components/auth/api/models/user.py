from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import DateTime, String

from datetime import datetime
from typing import List

from config import Base

from models import *


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(64))
    email: Mapped[str] = mapped_column(nullable=True)
    tokens: Mapped[List["Token"]] = relationship(
                                        "Token",
                                        back_populates="user",
                                        cascade="all, delete"
                                    )
    created_at: Mapped[DateTime] = mapped_column(
        DateTime, default=datetime.now()
    )
