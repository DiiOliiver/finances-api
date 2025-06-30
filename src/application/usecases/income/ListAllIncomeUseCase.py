from application.dto.PaginationDTO import PaginationDTO
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

        data_page = []
        user_ids = set(
            income['user_id']
            for income in pagination.data
            if 'user_id' in income
        )
        users_data = await self.user_repository.find_many_by_ids(
            list(user_ids)
        )
        users_lookup = {
            User(**user).model_dump()['id']: User(**user).model_dump()
            for user in users_data
        }

        for income in pagination.data:
            user_data = users_lookup.get(income.get('user_id'))
            if user_data is None:
                continue
            income['user'] = User(**user_data).model_dump()
            income.pop('user_id', None)
            data_page.append(income)
        pagination.data = data_page
        return pagination
