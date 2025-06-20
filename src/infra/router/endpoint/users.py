from typing import TypeVar

from dependency_injector.wiring import Provide, inject
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Request,
)
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
)

from application.dto.PaginationDTO import PaginationDTO
from application.dto.UserDTO import (
    CreateUserDTO,
    UpdateUserDTO,
    UserResponseDTO,
)
from application.usecases.user.CreateUserUseCase import CreateUserUseCase
from application.usecases.user.DeleteUserUseCase import DeleteUserUseCase
from application.usecases.user.FindByUserUseCase import FindByUserUseCase
from application.usecases.user.ListAllUserUseCase import ListAllUserUseCase
from application.usecases.user.UpdateUserUseCase import UpdateUserUseCase
from infra.di.Container import Container

router = APIRouter(prefix='/users', tags=['Users'])

T = TypeVar('T')


@router.post('', status_code=HTTP_201_CREATED, summary='Criação de usuário')
@inject
async def create_user(
    request: Request,
    data: CreateUserDTO,
    create_user_use_case: CreateUserUseCase = Depends(
        Provide[Container.create_user_use_case]
    ),
):
    try:
        user = await create_user_use_case.execute(data)
        return {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'created_at': user.created_at,
        }
    except ValueError as e:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(e))


@router.get('', status_code=HTTP_200_OK, summary='Lista páginavel de usuários')
@inject
async def read_users(
    request: Request,
    page: int = 1,
    per_page: int = 10,
    list_user_use_case: ListAllUserUseCase = Depends(
        Provide[Container.list_user_use_case]
    ),
) -> PaginationDTO:
    try:
        return await list_user_use_case.execute(page, per_page)
    except ValueError as e:
        print(e)
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(e))


@router.get('/{user_id}', status_code=HTTP_200_OK)
@inject
async def read_user(
    request: Request,
    user_id: str,
    find_by_user_use_case: FindByUserUseCase = Depends(
        Provide[Container.find_by_user_use_case]
    ),
):
    try:
        return await find_by_user_use_case.execute(user_id)
    except ValueError as e:
        print(e)
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(e))


@router.put('/{user_id}', status_code=HTTP_200_OK)
@inject
async def update_user(
    request: Request,
    user_id: str,
    data: UpdateUserDTO,
    update_user_use_case: UpdateUserUseCase = Depends(
        Provide[Container.update_user_use_case]
    ),
) -> UserResponseDTO:
    try:
        return await update_user_use_case.execute(user_id, data)
    except ValueError as e:
        print(e)
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete('/{user_id}', status_code=HTTP_200_OK)
@inject
async def delete_user(
    request: Request,
    user_id: str,
    delete_user_use_case: DeleteUserUseCase = Depends(
        Provide[Container.delete_user_use_case]
    ),
) -> bool:
    try:
        return await delete_user_use_case.execute(user_id)
    except ValueError as e:
        print(e)
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(e))
