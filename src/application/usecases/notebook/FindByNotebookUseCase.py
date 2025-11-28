from application.dto.NotebookDTO import NotebookResponseDTO
from application.dto.ResponseDTO import ResponseDTO, StatusEnum
from application.repositories.INotebookRepository import INotebookRepository
from application.repositories.IUserRepository import IUserRepository
from domain.models.Notebook import Notebook
from fastapi import HTTPException
from starlette.status import (
    HTTP_404_NOT_FOUND,
)


class FindByNotebookUseCase:
    def __init__(
        self,
        notebook_repository: INotebookRepository,
        user_repository: IUserRepository,
    ):
        self.notebook_repository = notebook_repository
        self.user_repository = user_repository

    async def execute(self, notebook_id: str) -> NotebookResponseDTO:
        notebook_data = await self.notebook_repository.find_by(notebook_id)
        if not notebook_data:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND,
                detail=ResponseDTO(
                    status=StatusEnum.FAIL,
                    message='A caderneta informada não existe.',
                ).model_dump(),
            )

        notebook_model = Notebook(**notebook_data).model_dump()

        return NotebookResponseDTO(**notebook_model)
