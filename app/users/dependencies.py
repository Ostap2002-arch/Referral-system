from datetime import datetime

from fastapi import Request, HTTPException, status, Depends
from jose import jwt, JWTError

from app.config import settings
from app.users.dao import UsersDAO


def get_token(request: Request):
    token = request.cookies.get('token_jwt')
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token missing')
    return token


async def get_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(token, key=settings.SECRET_KEY, algorithms=settings.ALGORITHM)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token missing')
    expire = payload.get('exp')
    if not expire and expire < datetime.utcnow().timestamp():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token expired')
    user_id = payload.get('user_id')
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token error')
    user = await UsersDAO.get_one_or_none(id=user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='The user was not found')
    return user
