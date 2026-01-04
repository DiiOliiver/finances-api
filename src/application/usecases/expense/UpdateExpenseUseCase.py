from http import HTTPStatus
from typing import Optional

from application.dto.ExpenseDTO import UpdateExpenseDTO
from application.dto.ResponseDTO import ResponseDTO, StatusEnum
from application.repositories.IExpenseRepository import IExpenseRepository
from domain.models.Expense import Expense
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder


class UpdateExpenseUseCase:
    def __init__(self, expense_repository: IExpenseRepository):
        self.expense_repository = expense_repository

    async def execute(
        self, expense_id: str, expense_new: UpdateExpenseDTO
    ) -> str:
        expense_data: Optional[dict] = await self.expense_repository.find_by(
            expense_id
        )
        if not expense_data:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=ResponseDTO(
                    status=StatusEnum.ERROR,
                    message='A despesa informada não existe.',
                ).model_dump(),
            )

        expense_data.update(expense_new.model_dump())
        expense = Expense(**expense_data)

        is_update = await self.expense_repository.update(
            expense_id, jsonable_encoder(expense)
        )
        if not is_update:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=ResponseDTO(
                    status=StatusEnum.FAIL,
                    message='Não foi possível alterar a despesa.',
                ).model_dump(),
            )
        return f'A despesa {f"{expense.description} " or ""}foi atualizada com sucesso.'
