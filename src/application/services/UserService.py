from pydantic import EmailStr

from application.repositories.IUserRepository import (
    IUserRepository,
)


class UserService:
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    async def is_email_taken(self, email: EmailStr) -> bool:
        user = await self.user_repository.get_by_email(email)
        return user is not None
