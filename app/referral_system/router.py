from datetime import timedelta, date
from typing import List

from fastapi import APIRouter, Depends, Form, HTTPException, status
from pydantic import EmailStr

from app.referral_system.dao import ReferralCodeDAO
from app.referral_system.shemas import SCreateRefCode
from app.referral_system.utils import create_new_code
from app.users.dao import UsersDAO
from app.users.dependencies import get_user
from app.users.models import UserModel
from app.users.shemas import SUserModel

router = APIRouter(
    prefix='/referral_system',
    tags=['Referral system']
)


@router.post('/create_code')
async def create_code(data: SCreateRefCode, user: UserModel = Depends(get_user)):
    if not data.code:
        data.code = create_new_code()
    if not data.expiration_date:
        data.expiration_date = date.today() + timedelta(days=30)
    result = await ReferralCodeDAO.add(
        code=data.code,
        expiration_date=data.expiration_date,
        owner_id=user.id,
    )
    return f'You have created a referral code {data.code}, which is valid until {data.expiration_date}'


@router.delete('/delete_code')
async def delete_code(id_code: int, user: UserModel = Depends(get_user)):
    code = await ReferralCodeDAO.get_one_or_none(id=id_code)
    if user.id != code.owner_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='You are not the owner of this code.')
    await ReferralCodeDAO.delete_by_id(id=code.id)
    return "You have successfully removed the code"


@router.post('/activate_code')
async def activate_code(code: str, user: UserModel = Depends(get_user)):
    code = await ReferralCodeDAO.get_one_or_none(code=code)
    all_user_codes = await ReferralCodeDAO.get_elements(owner_id=user.id)
    if not code:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Code not found')
    elif code.owner_id != user.id:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='You are not the owner of the code')
    elif code.activation:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='The code has already been activated')
    elif any(map(lambda x: x.activation, all_user_codes)):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='One of your codes is already active')
    else:
        await ReferralCodeDAO.update(code=code.code, activation=True)
    return f'{code.code} code activated'


@router.post('/deactivate_code')
async def deactivate_code(code: str, user: UserModel = Depends(get_user)):
    code = await ReferralCodeDAO.get_one_or_none(code=code)
    if not code:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Code not found')
    elif code.owner_id != user.id:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='You are not the owner of the code')
    elif not code.activation:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='This code is no longer deactivated.')
    else:
        await ReferralCodeDAO.update(code=code.code, activation=False)
    return f'{code.code} code deactivated'


@router.post('/get_referrals')
async def get_all_referrals(id: int, user: UserModel = Depends(get_user)) -> List[SUserModel]:
    referrals = await ReferralCodeDAO.get_all_referrals(id_referrer=id)
    return referrals


@router.get('/get_code')
async def get_code_by_email(email_referrer: EmailStr):
    referrer = await UsersDAO.get_one_or_none(email=email_referrer)
    if not referrer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User with such email not found')
    code = await ReferralCodeDAO.get_code_user(user=referrer)
    if not code:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='The specified user does not have referral codes or they are not active')
    return code.code
