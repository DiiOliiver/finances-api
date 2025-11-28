from application.dto.PaginationDTO import PaginationDTO
from application.repositories.IExpenseRepository import IExpenseRepository


class ListAllExpenseUseCase:
    def __init__(self, expense_repository: IExpenseRepository):
        self.expense_repository = expense_repository

    async def execute(self, page: int, per_page: int) -> PaginationDTO:
        page = 1 if page < 1 else page
        per_page = 10 if per_page < 1 else per_page
        return await self.expense_repository.paginate(page, per_page)
