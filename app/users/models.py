from datetime import datetime
from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base



class UserModel(Base):
    __tablename__ = 'Users'
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    hash_password: Mapped[str] = mapped_column(nullable=False)
    referrer_code_id: Mapped[int] = mapped_column(ForeignKey('Referral.id', name='User'), default=None, nullable=True)





