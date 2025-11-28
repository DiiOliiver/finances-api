from typing import Optional
from uuid import uuid4

from domain.models.Notebook import NotebookExpense
from pydantic import Field


class Expense(NotebookExpense):
    id: str = Field(default_factory=lambda: str(uuid4()), alias='_id')
    closing_day: Optional[str] = Field(None, description='Dia de fechamento')
    due_day: Optional[str] = Field(None, description='Dia do vencimento')
