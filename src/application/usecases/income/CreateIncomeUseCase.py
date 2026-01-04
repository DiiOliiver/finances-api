import logging
from datetime import datetime
from http import HTTPStatus

from application.dto.IncomeDTO import CreateIncomeDTO
from application.dto.ResponseDTO import ResponseDTO, StatusEnum
from application.repositories.IIncomeRepository import IIncomeRepository
from domain.models.Income import Income
from fastapi import HTTPException

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CreateIncomeUseCase:
    def __init__(
        self,
        income_repository: IIncomeRepository,
    ):
        self.income_repository = income_repository

    async def execute(self, data: CreateIncomeDTO) -> str:
        try:
            income = Income(
                user_id=data.user_id,
                amount=data.amount,
                income_day=data.income_day,
                category=data.category,
                description=data.description,
                created_at=datetime.utcnow(),
                updated_at=None,
            )
            await self.income_repository.add(income)
            return f'Renda {income.amount} da categoria {income.category} foi cadastrada com sucesso.'
        except Exception as exc:
            logging.error(f'Erro ao cadastrar renda: {exc}')
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=ResponseDTO(
                    status=StatusEnum.FAIL,
                    message='Erro ao cadastrar renda.',
                ).model_dump(),
            )
