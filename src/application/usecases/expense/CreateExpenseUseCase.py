import logging
from http import HTTPStatus

from application.dto.ExpenseDTO import CreateExpenseDTO
from application.dto.ResponseDTO import ResponseDTO, StatusEnum
from application.repositories.IExpenseRepository import IExpenseRepository
from domain.models.Expense import Expense
from fastapi import HTTPException

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CreateExpenseUseCase:
    def __init__(self, expense_repository: IExpenseRepository, user_id: str):
        self.expense_repository = expense_repository
        self.user_id = user_id

    async def execute(self, data: CreateExpenseDTO) -> str:
        try:
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
        except Exception as exc:
            logger.error(f'Erro ao criar despesa fixa: {exc}')
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=ResponseDTO(
                    status=StatusEnum.FAIL,
                    message='Erro ao criar despesa fixa.',
                ).model_dump(),
            )
