from application.dto.ResponseDTO import ResponseDTO, StatusEnum
from application.dto.UserDTO import UserResponseDTO
from application.repositories.IUserRepository import (
    IUserRepository,
)
from domain.models.User import User
from fastapi import HTTPException
from starlette.status import HTTP_404_NOT_FOUND


class FindByUserUseCase:
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    async def execute(self, user_id: str) -> UserResponseDTO:
        user_data = await self.user_repository.find_by(user_id)
        if not user_data:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND,
                detail=ResponseDTO(
                    status=StatusEnum.FAIL,
                    message='Usuário informado não existe.',
                ).model_dump(),
            )
        user_model = User(**user_data).model_dump()
        return UserResponseDTO(**user_model)
