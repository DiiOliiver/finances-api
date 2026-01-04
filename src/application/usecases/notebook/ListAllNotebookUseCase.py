from typing import Dict, List

from application.dto.ExpenseDTO import ExpenseResponseDTO
from application.dto.NotebookDTO import NotebookResponseDTO
from application.dto.PaginationDTO import PaginationDTO
from application.repositories.INotebookRepository import INotebookRepository
from application.repositories.IUserRepository import IUserRepository
from domain.models.Expense import Expense


class ListAllNotebookUseCase:
    def __init__(
        self,
        notebook_repository: INotebookRepository,
        user_repository: IUserRepository,
    ):
        self.notebook_repository = notebook_repository
        self.user_repository = user_repository

    async def execute(self, page: int, per_page: int) -> PaginationDTO:
        page = 1 if page < 1 else page
        per_page = 10 if per_page < 1 else per_page

        pagination = await self.notebook_repository.paginate(page, per_page)

        data_page: List[Dict] = []
        for data in pagination.data:
            notebook_dto: Dict = NotebookResponseDTO(**data).model_dump()
            expenses: List[Dict] = self._mounted_expense(notebook_dto)
            notebook_dto.update({'expenses': expenses})
            data_page.append(notebook_dto)

        pagination.data = data_page

        return pagination

    @staticmethod
    def _mounted_expense(notebook_dto: Dict) -> List[Dict]:
        return [
            ExpenseResponseDTO(**Expense(**expense).model_dump()).model_dump()
            for expense in notebook_dto.get('expenses', [])
        ]
