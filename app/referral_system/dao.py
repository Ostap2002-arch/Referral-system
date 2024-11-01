from datetime import date, datetime

from fastapi import HTTPException, status
from sqlalchemy import select, update, and_

from app.dao.base import BaseDAO
from app.database import session_maker
from app.referral_system.models import ReferralModel
from app.users.models import UserModel


class ReferralCodeDAO(BaseDAO):
    model = ReferralModel

    @classmethod
    async def update(cls, code: str, **values):
        async with session_maker() as session:
            stmt = update(cls.model).filter_by(code=code).values(**values)
            await session.execute(stmt)
            await session.commit()

    @classmethod
    async def check_code(cls, code):
        code = await cls.get_one_or_none(code=code)
        if not code:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Referral code not found')
        elif not code.activation:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='The code is not active')
        elif code.expiration_date < datetime.today():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='The code has expired')
        else:
            return code

    @classmethod
    async def get_all_referrals(cls, id_referrer: int):
        async with session_maker() as session:
            query = select(UserModel).select_from(UserModel
                                                  ).join(ReferralModel, ReferralModel.id == UserModel.referrer_code_id, isouter=True
                                                                  ).where(ReferralModel.owner_id == id_referrer)
            results = await session.execute(query)
            results = results.scalars()
            return results


    @classmethod
    async def get_code_user(cls, user: UserModel):
        async with session_maker() as session:
            query = select(ReferralModel).where(and_(ReferralModel.owner_id == user.id, ReferralModel.activation))
            result = await session.execute(query)
            return result.scalar_one_or_none()
