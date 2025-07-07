from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from domain.models.enum.ExpenseStatus import ExpenseStatus


class NotebookCommentDTO(BaseModel):
    message: str
    user_id: str


class NotebookExpense(BaseModel):
    amount: float
    closing_day: Optional[str] = None
    due_day: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    status: ExpenseStatus


class CreateNotebookDTO(BaseModel):
    title: str
    description: Optional[str] = None
    users: Optional[List[str]] = None


class UpdateNotebookDTO(CreateNotebookDTO):
    comments: Optional[List[NotebookCommentDTO]] = None
    expenses: Optional[List[NotebookExpense]] = None


class NotebookResponseDTO(UpdateNotebookDTO):
    id: str
    created_at: datetime
    updated_at: Optional[datetime] = None
