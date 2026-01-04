import logging
from datetime import datetime
from http import HTTPStatus

from application.dto.ResponseDTO import ResponseDTO, StatusEnum
from application.dto.UserDTO import CreateUserDTO
from application.gateway import IUserGateway
from application.repositories.IUserRepository import IUserRepository
from application.services.UserService import UserService
from domain.models.User import User
from fastapi import HTTPException

from security import get_password_hash

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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

    async def execute(self, data: CreateUserDTO) -> str:
        if await self.user_service.is_email_taken(data.email):
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail=ResponseDTO(
                    status=StatusEnum.FAIL,
                    message=f'Usuário {data.name} já existe.',
                ).model_dump(),
            )

        try:
            hashed_password = get_password_hash(data.password)

            user = User(
                name=data.name,
                email=data.email,
                status=True,
                password=hashed_password,
                created_at=datetime.utcnow(),
                updated_at=None,
            )
            await self.user_repository.add(user)

            await self.user_gateway.send_welcome_email(user.email, user.name)

            return f'Usuário {user.name} cadastrado com sucesso.'
        except Exception as exc:
            logger.error(f'Erro ao criar usuário: {exc}')
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=ResponseDTO(
                    status=StatusEnum.FAIL,
                    message='Erro ao criar usuário.',
                ).model_dump(),
            )
