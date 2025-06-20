from application.dto.UserDTO import CreateUserDTO
from application.gateway import IUserGateway
from application.repositories.IUserRepository import IUserRepository
from application.services.UserService import UserService
from domain.models.User import User


class CreateUserUseCase:
    def __init__(
        self,
        user_service: UserService,
        user_gateway: IUserGateway,
        user_repository: IUserRepository,
    ):
        self.user_service = user_service
        self.user_gateway = user_gateway
        self.user_repository = user_repository

    async def execute(self, data: CreateUserDTO) -> User:
        if await self.user_service.is_email_taken(data.email):
            raise ValueError('User already exists')

        user = User.create(name=data.name, email=data.email)
        await self.user_repository.add(user)

        await self.user_gateway.send_welcome_email(user.email, user.name)

        return user
