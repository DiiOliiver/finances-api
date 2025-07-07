from application.dto.NotebookDTO import CreateNotebookDTO
from application.repositories.INotebookRepository import INotebookRepository
from domain.models.Notebook import Notebook


class CreateNotebookUseCase:
    def __init__(self, notebook_repository: INotebookRepository, user_id: str):
        self.notebook_repository = notebook_repository
        self.user_id = user_id

    async def execute(self, data: CreateNotebookDTO) -> str:
        notebook = Notebook(
            title=data.title,
            description=data.description,
            users=data.users,
            created_by=self.user_id,
        )
        await self.notebook_repository.add(notebook)
        return f'Caderneta {notebook.title} foi cadastrada com sucesso.'
