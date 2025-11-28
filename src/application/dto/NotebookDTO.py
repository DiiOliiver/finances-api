from datetime import datetime
from typing import List, Optional

from application.dto.ExpenseDTO import CreateExpenseDTO
from pydantic import BaseModel


class NotebookCommentDTO(BaseModel):
    message: str
    user_id: str


class CreateNotebookDTO(BaseModel):
    title: str
    description: Optional[str] = None
    users: Optional[List[str]] = None


class UpdateNotebookDTO(CreateNotebookDTO):
    comments: Optional[List[NotebookCommentDTO]] = None
    expenses: Optional[List[CreateExpenseDTO]] = None


class NotebookResponseDTO(UpdateNotebookDTO):
    id: str
    created_at: datetime
    updated_at: Optional[datetime] = None
