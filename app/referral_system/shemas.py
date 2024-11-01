from datetime import date
from typing import Optional

from pydantic import BaseModel, Field


class SCreateRefCode(BaseModel):
    code: Optional[str] = Field(None, min_length=9)
    expiration_date: Optional[date] = Field(None, ge=date.today())

