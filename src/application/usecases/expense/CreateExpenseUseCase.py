from application.dto.ExpenseDTO import CreateExpenseDTO
from application.repositories.IExpenseRepository import IExpenseRepository
from domain.models.Expense import Expense


class CreateExpenseUseCase:
    def __init__(self, expense_repository: IExpenseRepository, user_id: str):
        self.expense_repository = expense_repository
        self.user_id = user_id

    async def execute(self, data: CreateExpenseDTO) -> str:
        expense = Expense(
            amount=data.amount,
            closing_day=data.closing_day,
            due_day=data.due_day,
            category=data.category,
            description=data.description,
            status=data.status,
            created_by=self.user_id,
        )
        await self.expense_repository.add(expense)
        return (
            f'Despesa fixa com valor R$ {expense.amount} com data '
            f'de vencimento todo dia {expense.due_day} foi cadastrado.'
        )
