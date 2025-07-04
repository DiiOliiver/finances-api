from typing import Optional

from pydantic import BaseModel

from application.dto.UserDTO import UserResponseDTO


class CreateIncomeDTO(BaseModel):
    user_id: str
    amount: float
    income_day: str
    category: Optional[str] = None
    description: Optional[str] = None


class UpdateIncomeDTO(BaseModel):
    amount: float
    income_day: str
    category: Optional[str] = None
    description: Optional[str] = None


class IncomeResponseDTO(BaseModel):
    id: str
    user: UserResponseDTO
    amount: float
    income_day: str
    category: Optional[str] = None
    description: Optional[str] = None
