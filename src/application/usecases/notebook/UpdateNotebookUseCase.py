from typing import Optional

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

from application.dto.NotebookDTO import UpdateNotebookDTO
from application.dto.ResponseDTO import ResponseDTO, StatusEnum
from application.repositories.INotebookRepository import INotebookRepository
from domain.models.Notebook import Notebook


class UpdateNotebookUseCase:
    def __init__(self, notebook_repository: INotebookRepository):
        self.notebook_repository = notebook_repository

    async def execute(
        self, notebook_id: str, notebook_new: UpdateNotebookDTO
    ) -> str:
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

        notebook_data.update(notebook_new.model_dump())
        notebook_old = Notebook(**notebook_data)

        is_update = await self.notebook_repository.update(
            notebook_id, jsonable_encoder(notebook_old)
        )
        if not is_update:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail=ResponseDTO(
                    status=StatusEnum.FAIL,
                    message='Não foi possível alterar a caderneta.',
                ).model_dump(),
            )
        return f'A caderneta {notebook_old.title} foi atualizada com sucesso.'
