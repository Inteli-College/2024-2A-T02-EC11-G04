from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import DateTime

from datetime import datetime

from config import Base
from models import *


class Token(Base):
    __tablename__ = "tokens"

    id: Mapped[int] = mapped_column(primary_key=True)
    token: Mapped[str]
    expiration: Mapped[datetime]  
    revoked_token: Mapped[bool] = mapped_column(default=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    user: Mapped["User"] = relationship("User", back_populates="tokens")
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now()
    )
