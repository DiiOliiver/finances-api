from datetime import datetime

from fastapi.encoders import jsonable_encoder

from application.dto.UserDTO import UpdateUserDTO, UserResponseDTO
from application.repositories.IUserRepository import IUserRepository
from application.services.UserService import UserService


class UpdateUserUseCase:
    def __init__(
        self, user_service: UserService, user_repository: IUserRepository
    ):
        self.user_service = user_service
        self.user_repository = user_repository

    async def execute(self, user_id: str, user_new: UpdateUserDTO) -> str:
        user_old = await self.user_repository.find_by(user_id, UserResponseDTO)

        if (
            user_old.email != user_new.email
        ) & await self.user_service.is_email_taken(user_new.email):
            raise ValueError('Email already exists')

        self._update_users(user_old, user_new)

        user_data = jsonable_encoder(user_old)

        user: UserResponseDTO = await self.user_repository.update(
            user_id, user_data
        )
        return user.name

    @staticmethod
    def _update_users(user_old, user_new):
        user_old.name = user_new.name
        user_old.email = user_new.email
        user_old.status = user_new.status
        user_old.updated_at = datetime.utcnow()
