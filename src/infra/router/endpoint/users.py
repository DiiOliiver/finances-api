from dependency_injector.wiring import Provide, inject
from fastapi import (
    APIRouter,
    Depends,
    Request,
)
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
)

from application.dto.PaginationDTO import PaginationDTO
from application.dto.ResponseDTO import ResponseDTO, StatusEnum
from application.dto.UserDTO import (
    CreateUserDTO,
    UpdateUserDTO,
)
from application.usecases.user.CreateUserUseCase import CreateUserUseCase
from application.usecases.user.DeleteUserUseCase import DeleteUserUseCase
from application.usecases.user.FindByUserUseCase import FindByUserUseCase
from application.usecases.user.ListAllUserUseCase import ListAllUserUseCase
from application.usecases.user.UpdateUserUseCase import UpdateUserUseCase
from application.utils.error_handler import error_handler
from infra.di.Container import Container

router = APIRouter(prefix='/users', tags=['Users'])


@router.post('', status_code=HTTP_201_CREATED, summary='Cadastro de usuário')
@inject
@error_handler
async def create_user(
    request: Request,
    data: CreateUserDTO,
    create_user_use_case: CreateUserUseCase = Depends(
        Provide[Container.create_user_use_case]
    ),
) -> ResponseDTO:
    message_response = await create_user_use_case.execute(data)
    return ResponseDTO(
        status=StatusEnum.SUCCESS,
        message=message_response,
    )


@router.get('', status_code=HTTP_200_OK, summary='Lista páginavel de usuários')
@inject
@error_handler
async def read_users(
    request: Request,
    page: int = 1,
    per_page: int = 10,
    list_user_use_case: ListAllUserUseCase = Depends(
        Provide[Container.list_user_use_case]
    ),
) -> ResponseDTO:
    pagination: PaginationDTO = await list_user_use_case.execute(
        page, per_page
    )
    return ResponseDTO(status=StatusEnum.SUCCESS, data=pagination.dict())


@router.get('/{user_id}', status_code=HTTP_200_OK, summary='Consulta usuário')
@inject
@error_handler
async def read_user(
    request: Request,
    user_id: str,
    find_by_user_use_case: FindByUserUseCase = Depends(
        Provide[Container.find_by_user_use_case]
    ),
):
    user = await find_by_user_use_case.execute(user_id)
    return ResponseDTO(status=StatusEnum.SUCCESS, data=user.dict())


@router.put('/{user_id}', status_code=HTTP_200_OK, summary='Atualizar usuário')
@inject
@error_handler
async def update_user(
    request: Request,
    user_id: str,
    data: UpdateUserDTO,
    update_user_use_case: UpdateUserUseCase = Depends(
        Provide[Container.update_user_use_case]
    ),
) -> ResponseDTO:
    message_response = await update_user_use_case.execute(user_id, data)
    return ResponseDTO(
        status=StatusEnum.SUCCESS,
        message=message_response,
    )


@router.delete(
    '/{user_id}', status_code=HTTP_200_OK, summary='Remover usuário'
)
@inject
@error_handler
async def delete_user(
    request: Request,
    user_id: str,
    delete_user_use_case: DeleteUserUseCase = Depends(
        Provide[Container.delete_user_use_case]
    ),
) -> ResponseDTO:
    message_response = await delete_user_use_case.execute(user_id)
    return ResponseDTO(
        status=StatusEnum.SUCCESS,
        message=message_response,
    )
