from datetime import datetime

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

from application.dto.ResponseDTO import ResponseDTO, StatusEnum
from application.dto.UserDTO import UpdateUserDTO
from application.repositories.IUserRepository import IUserRepository
from application.services.UserService import UserService
from domain.models.User import User


class UpdateUserUseCase:
    def __init__(
        self, user_service: UserService, user_repository: IUserRepository
    ):
        self.user_service = user_service
        self.user_repository = user_repository

    async def execute(self, user_id: str, user_new: UpdateUserDTO) -> str:
        user_data = await self.user_repository.find_by(user_id)
        if not user_data:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND,
                detail=ResponseDTO(
                    status=StatusEnum.FAIL,
                    message='Usuário informado não existe.',
                ).model_dump(),
            )
        user_old = User(**user_data)

        if (
            user_old.email != user_new.email
        ) & await self.user_service.is_email_taken(user_new.email):
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail=ResponseDTO(
                    status=StatusEnum.FAIL,
                    message='Usuário informado já existe.',
                ).model_dump(),
            )

        user_old.name = user_new.name
        user_old.email = user_new.email
        user_old.status = user_new.status
        user_old.updated_at = datetime.utcnow()

        is_update = await self.user_repository.update(
            user_id, jsonable_encoder(user_old)
        )
        if not is_update:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail=ResponseDTO(
                    status=StatusEnum.FAIL,
                    message='Não foi possível alterar o usuário.',
                ).model_dump(),
            )

        return f'Usuário {user_old.name} atualizado com sucesso.'
