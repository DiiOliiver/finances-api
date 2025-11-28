from typing import Optional

from application.dto.ResponseDTO import ResponseDTO, StatusEnum
from application.repositories.IUserRepository import IUserRepository
from domain.models.User import User
from fastapi import HTTPException
from starlette.status import HTTP_404_NOT_FOUND


class DeleteUserUseCase:
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    async def execute(self, user_id: str) -> str:
        user_data: Optional[dict] = await self.user_repository.find_by(user_id)
        if not user_data:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND,
                detail=ResponseDTO(
                    status=StatusEnum.FAIL,
                    message='O usuário informado não existe.',
                ).model_dump(),
            )
        await self.user_repository.delete(user_id)
        user_model = User(**user_data)
        return f'Usuário {user_model.name} foi removido com sucesso.'
