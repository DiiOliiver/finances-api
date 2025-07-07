from typing import Optional

from pydantic import BaseModel, Field

from domain.models.enum.ExpenseStatus import ExpenseStatus


class NotebookExpense(BaseModel):
    amount: float = Field(..., description='Valor da despesa')
    closing_day: Optional[str] = Field(None, description='Dia de fechamento')
    due_day: Optional[str] = Field(None, description='Dia do vencimento')
    category: Optional[str] = Field(None, description='Categoria')
    description: Optional[str] = Field(None, description='Descrição')
    status: ExpenseStatus = Field(..., description='Status da despesa')
