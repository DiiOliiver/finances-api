from typing import Dict, List, Optional

from application.dto.PaginationDTO import PaginationDTO
from application.dto.UserDTO import UserResponseDTO
from application.repositories.IIncomeRepository import IIncomeRepository
from application.repositories.IUserRepository import IUserRepository
from domain.models.User import User


class ListAllIncomeUseCase:
    def __init__(
        self,
        income_repository: IIncomeRepository,
        user_repository: IUserRepository,
    ):
        self.income_repository = income_repository
        self.user_repository = user_repository

    async def execute(self, page: int, per_page: int) -> PaginationDTO:
        page = 1 if page < 1 else page
        per_page = 10 if per_page < 1 else per_page
        pagination = await self.income_repository.paginate(page, per_page)

        data_page: List[Dict] = []
        for data in pagination.data:
            users_data: Optional[dict] = await self.user_repository.find_by(
                data.get('user_id')
            )
            data.update({
                'user': UserResponseDTO(**User(**users_data).model_dump())
            })
            data.pop('user_id', None)
            data_page.append(data)

        pagination.data = data_page
        return pagination
