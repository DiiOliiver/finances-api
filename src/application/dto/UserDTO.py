import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class CreateUserDTO(BaseModel):
    name: str
    email: EmailStr


class UpdateUserDTO(CreateUserDTO):
    status: bool


class UserResponseDTO(BaseModel):
    id: str
    name: str
    email: EmailStr
    status: bool
    created_at: datetime.datetime
    updated_at: Optional[datetime.datetime]
