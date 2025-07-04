from typing import Optional

from fastapi import HTTPException
from starlette.status import HTTP_404_NOT_FOUND

from application.dto.ResponseDTO import ResponseDTO, StatusEnum
from application.repositories.IIncomeRepository import IIncomeRepository
from domain.models.Income import Income


class DeleteIncomeUseCase:
    def __init__(self, income_repository: IIncomeRepository):
        self.income_repository = income_repository

    async def execute(self, income_id: str) -> str:
        income_data: Optional[dict] = await self.income_repository.find_by(
            income_id
        )
        if not income_data:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND,
                detail=ResponseDTO(
                    status=StatusEnum.FAIL,
                    message='A renda informada não existe.',
                ).model_dump(),
            )
        await self.income_repository.delete(income_id)
        income_model = Income(**income_data)
        return f'Renda {income_model.amount} da categoria {income_model.category} foi removida com sucesso.'
