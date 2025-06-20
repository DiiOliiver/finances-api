from application.dto.UserDTO import UserResponseDTO
from application.repositories.IUserRepository import (
    IUserRepository,
)


class FindByUserUseCase:
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    async def execute(self, user_id: str) -> UserResponseDTO:
        return await self.user_repository.find_by(user_id, UserResponseDTO)
