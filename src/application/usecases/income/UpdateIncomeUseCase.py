from datetime import datetime
from typing import Optional

from application.dto.IncomeDTO import UpdateIncomeDTO
from application.dto.ResponseDTO import ResponseDTO, StatusEnum
from application.repositories.IIncomeRepository import IIncomeRepository
from domain.models.Income import Income
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND


class UpdateIncomeUseCase:
    def __init__(self, income_repository: IIncomeRepository):
        self.income_repository = income_repository

    async def execute(
        self, income_id: str, income_new: UpdateIncomeDTO
    ) -> str:
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

        income_old = Income(**income_data)
        income_old.amount = income_new.amount
        income_old.income_day = income_new.income_day
        income_old.category = income_new.category
        income_old.description = income_new.description
        income_old.updated_at = datetime.utcnow()

        is_update = await self.income_repository.update(
            income_id, jsonable_encoder(income_old)
        )
        if not is_update:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail=ResponseDTO(
                    status=StatusEnum.FAIL,
                    message='Não foi possível alterar a renda.',
                ).model_dump(),
            )
        return f'Renda {income_old.amount} da categoria {income_old.category} foi atualizada com sucesso.'
