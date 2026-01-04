import logging
from http import HTTPStatus

from application.dto.NotebookDTO import CreateNotebookDTO
from application.dto.ResponseDTO import ResponseDTO, StatusEnum
from application.repositories.INotebookRepository import INotebookRepository
from domain.models.Notebook import Notebook
from fastapi import HTTPException

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CreateNotebookUseCase:
    def __init__(self, notebook_repository: INotebookRepository, user_id: str):
        self.notebook_repository = notebook_repository
        self.user_id = user_id

    async def execute(self, data: CreateNotebookDTO) -> str:
        try:
            notebook = Notebook(
                title=data.title,
                description=data.description,
                users=data.users,
                created_by=self.user_id,
            )
            await self.notebook_repository.add(notebook)
            return f'Caderneta {notebook.title} foi cadastrada com sucesso.'
        except Exception as exc:
            logging.error(f'Erro ao cadastrar caderneta: {exc}')
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=ResponseDTO(
                    status=StatusEnum.FAIL,
                    message='Erro ao cadastrar caderneta.',
                ).model_dump(),
            )
