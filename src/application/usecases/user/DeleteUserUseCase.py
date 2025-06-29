from application.dto.UserDTO import UserResponseDTO
from application.repositories.IUserRepository import IUserRepository


class DeleteUserUseCase:
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    async def execute(self, user_id: str) -> str:
        user = await self.user_repository.find_by(user_id, UserResponseDTO)
        await self.user_repository.delete(user_id)
        return user.name
