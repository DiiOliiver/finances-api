from application.dto.NotebookDTO import NotebookResponseDTO
from application.dto.PaginationDTO import PaginationDTO
from application.dto.UserDTO import CreateUserDTO
from application.repositories.INotebookRepository import INotebookRepository
from application.repositories.IUserRepository import IUserRepository


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

        # Trata None ou ausência de 'users' como lista vazia
        user_ids = {
            user_id
            for notebook in pagination.data
            for user_id in (notebook.get('users') or [])
        }

        users_lookup = {}
        if user_ids:
            users_data = await self.user_repository.find_many_by_ids(
                list(user_ids)
            )
            users_lookup = {
                user['_id']: CreateUserDTO(**user) for user in users_data
            }

        notebook_data = []
        for notebook in pagination.data:
            notebook_dto = NotebookResponseDTO(**notebook).model_dump()
            notebook_dto['users'] = [
                users_lookup[user_id]
                for user_id in (notebook.get('users') or [])
                if user_id in users_lookup
            ]
            notebook_data.append(notebook_dto)

        pagination.data = notebook_data

        return pagination
