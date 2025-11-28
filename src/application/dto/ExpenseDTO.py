from datetime import datetime
from typing import Optional

from domain.models.enum.ExpenseStatus import ExpenseStatus
from pydantic import BaseModel


class CreateExpenseDTO(BaseModel):
    amount: float
    closing_day: Optional[str] = None
    due_day: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    status: ExpenseStatus


class ExpenseResponseDTO(CreateExpenseDTO):
    id: str
    created_at: datetime
    updated_at: Optional[datetime] = None


class UpdateExpenseDTO(CreateExpenseDTO):
    closing_day: Optional[str] = None
    due_day: Optional[str] = None
