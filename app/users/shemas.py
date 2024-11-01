from typing import Optional

from pydantic import BaseModel, EmailStr


class SUserDataRegister(BaseModel):
    email: EmailStr
    password: str
    referral_code: Optional[str] = None


class SUserData(BaseModel):
    email: EmailStr
    password: str


class SUserModel(BaseModel):
    id: int
    email: EmailStr
    hash_password: str
    referrer_code_id: int
