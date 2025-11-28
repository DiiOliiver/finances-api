from application.dto.ExpenseDTO import ExpenseResponseDTO
from application.dto.ResponseDTO import ResponseDTO, StatusEnum
from application.repositories.IExpenseRepository import IExpenseRepository
from domain.models.Expense import Expense
from fastapi import HTTPException
from starlette.status import (
    HTTP_404_NOT_FOUND,
)


class FindByExpenseUseCase:
    def __init__(self, expense_repository: IExpenseRepository):
        self.expense_repository = expense_repository

    async def execute(self, expense_id: str) -> ExpenseResponseDTO:
        expense_data = await self.expense_repository.find_by(expense_id)
        if not expense_data:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND,
                detail=ResponseDTO(
                    status=StatusEnum.FAIL,
                    message='A despesa informada não existe.',
                ).model_dump(),
            )

        expense_model = Expense(**expense_data).model_dump()

        return ExpenseResponseDTO(**expense_model)
