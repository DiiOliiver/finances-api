from typing import Optional

from application.dto.ResponseDTO import ResponseDTO, StatusEnum
from application.repositories.INotebookRepository import INotebookRepository
from domain.models.Notebook import Notebook
from fastapi import HTTPException
from starlette.status import HTTP_404_NOT_FOUND


class DeleteNotebookUseCase:
    def __init__(self, notebook_repository: INotebookRepository):
        self.notebook_repository = notebook_repository

    async def execute(self, notebook_id: str) -> str:
        notebook_data: Optional[dict] = await self.notebook_repository.find_by(
            notebook_id
        )
        if not notebook_data:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND,
                detail=ResponseDTO(
                    status=StatusEnum.FAIL,
                    message='A caderneta informada não existe.',
                ).model_dump(),
            )
        await self.notebook_repository.delete(notebook_id)
        notebook_model = Notebook(**notebook_data)
        return f'A caderneta {notebook_model.title} foi removida com sucesso.'
