from datetime import datetime

from application.dto.IncomeDTO import CreateIncomeDTO
from application.repositories.IIncomeRepository import IIncomeRepository
from domain.models.Income import Income


class CreateIncomeUseCase:
    def __init__(
        self,
        income_repository: IIncomeRepository,
    ):
        self.income_repository = income_repository

    async def execute(self, data: CreateIncomeDTO) -> str:
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
