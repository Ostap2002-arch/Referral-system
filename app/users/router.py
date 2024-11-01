from fastapi import APIRouter, HTTPException, status, Response, Depends

from app.referral_system.dao import ReferralCodeDAO
from app.users.auth import get_hash_password, verify_password, create_access_token
from app.users.dao import UsersDAO
from app.users.dependencies import get_user
from app.users.models import UserModel
from app.users.shemas import SUserData, SUserDataRegister

router = APIRouter(
    prefix='/auth',
    tags=['Auth and Users']
)


@router.post('/register')
async def register(data: SUserDataRegister):
    check_mail = await UsersDAO.get_one_or_none(email=data.email)
    if check_mail:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='User with such an email already exists')
    hash_password = get_hash_password(data.password)
    if data.referral_code:
        code = await ReferralCodeDAO.check_code(data.referral_code)
        await UsersDAO.add(email=data.email, hash_password=hash_password, referrer_code_id=code.id)
    else:
        await UsersDAO.add(email=data.email, hash_password=hash_password)
    return 'You have successfully registered'


@router.post('/login')
async def login(data: SUserData, response: Response):
    user = await UsersDAO.get_one_or_none(email=data.email)
    if not user or not verify_password(data.password, user.hash_password):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail='The email or password was entered incorrectly')

    token_jwt = create_access_token(data={"user_id": user.id})
    response.set_cookie('token_jwt', token_jwt)
    return 'Authentication is complete'


@router.post('/logout')
async def logout(response: Response, user: UserModel = Depends(get_user)):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='You are not logged in')
    response.delete_cookie('token_jwt')
    return 'You are out'
