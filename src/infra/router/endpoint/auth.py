from http import HTTPStatus

from application.dto.LoginDTO import LoginDTO
from application.dto.ResponseDTO import ResponseDTO, StatusEnum
from application.dto.TokenDTO import TokenDTO
from application.usecases.auth.LoginForAccessTokenUseCase import (
    LoginForAccessTokenUseCase,
)
from application.utils.error_handler import error_handler
from dependency_injector.wiring import Provide, inject
from fastapi import (
    APIRouter,
    Depends,
    Request,
)
from infra.di.Container import Container

router = APIRouter(prefix='/auth', tags=['Auth'])


@router.post(
    '/token',
    status_code=HTTPStatus.CREATED,
    summary='Gerar token de acesso',
    response_model=TokenDTO,
)
@inject
@error_handler
async def login_for_access_token(
    request: Request,
    form_data: LoginDTO,
    login_for_access_token_use_case: LoginForAccessTokenUseCase = Depends(
        Provide[Container.login_for_access_token_use_case]
    ),
) -> ResponseDTO:
    access_token: str = await login_for_access_token_use_case.execute(
        form_data
    )
    token_dto: TokenDTO = TokenDTO(
        access_token=access_token, token_type='bearer'
    )
    return ResponseDTO(
        status=StatusEnum.SUCCESS,
        data=token_dto,
        message='Token de acesso gerado com sucesso.',
    )
