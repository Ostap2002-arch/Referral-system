from datetime import datetime
from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.users.models import UserModel

class ReferralModel(Base):
    __tablename__ = 'Referral'
    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(nullable=False, unique=True)
    expiration_date: Mapped[datetime] = mapped_column(nullable=False)
    owner_id: Mapped[int] = mapped_column(ForeignKey('Users.id', name='Ref'))
    activation: Mapped[bool] = mapped_column(nullable=True, default=False)
