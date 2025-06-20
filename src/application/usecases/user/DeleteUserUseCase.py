from application.repositories.IUserRepository import IUserRepository


class DeleteUserUseCase:
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    async def execute(self, user_id: str) -> bool:
        return await self.user_repository.delete(user_id)
