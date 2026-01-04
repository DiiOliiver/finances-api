from http import HTTPStatus

from application.dto.LoginDTO import LoginDTO
from application.dto.ResponseDTO import ResponseDTO, StatusEnum
from application.repositories.IUserRepository import IUserRepository
from domain.models.User import User
from fastapi import HTTPException
from pydantic import EmailStr

from security import create_access_token, verify_password


class LoginForAccessTokenUseCase:
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    async def execute(self, form_data: LoginDTO):
        username: EmailStr | str = form_data.username
        user: User = await self.user_repository.get_by_email(email=username)

        if not user:
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail=ResponseDTO(
                    status=StatusEnum.FAIL,
                    message='Nome de usuário ou senha incorretos',
                ).model_dump(),
            )

        if not verify_password(form_data.password, user.password):
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail=ResponseDTO(
                    status=StatusEnum.FAIL,
                    message='E-mail ou senha incorretos',
                ).model_dump(),
            )

        data = {'sub': user.email, 'name': user.name, 'email': user.email}
        access_token = create_access_token(data=data)

        return access_token
