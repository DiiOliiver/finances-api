from typing import Optional

from application.dto.ResponseDTO import ResponseDTO, StatusEnum
from application.repositories.IExpenseRepository import IExpenseRepository
from fastapi import HTTPException
from starlette.status import HTTP_404_NOT_FOUND


class DeleteExpenseUseCase:
    def __init__(self, expense_repository: IExpenseRepository):
        self.expense_repository = expense_repository

    async def execute(self, expense_id: str) -> str:
        expense_data: Optional[dict] = await self.expense_repository.find_by(
            expense_id
        )
        if not expense_data:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND,
                detail=ResponseDTO(
                    status=StatusEnum.FAIL,
                    message='A despesa informada não existe.',
                ).model_dump(),
            )
        await self.expense_repository.delete(expense_id)
        return 'A despesa foi removida com sucesso.'
