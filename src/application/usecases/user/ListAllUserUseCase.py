from application.dto.PaginationDTO import PaginationDTO
from application.repositories.IUserRepository import (
    IUserRepository,
)


class ListAllUserUseCase:
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    async def execute(self, page: int, per_page: int) -> PaginationDTO:
        page = 1 if page < 1 else page
        per_page = 10 if per_page < 1 else per_page
        return await self.user_repository.paginate(page, per_page)
