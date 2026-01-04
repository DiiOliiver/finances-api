from http import HTTPStatus

from application.dto.ResponseDTO import ResponseDTO, StatusEnum
from application.usecases.extract import CreateExtractUseCase
from application.utils.error_handler import error_handler
from dependency_injector.wiring import Provide, inject
from domain.CurrentUser import CurrentUser
from domain.models.enum.RoleActions import RoleActions
from domain.models.enum.RolePermissions import RolePermissions
from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    Request,
    UploadFile,
)
from infra.di.Container import Container
from infra.middleware.ValidateRolesDecorator import validate_role

router = APIRouter(prefix='/extracts', tags=['Extracts'])


@router.post(
    '/upload-csv',
    status_code=HTTPStatus.CREATED,
    summary='Upload de extrato bancário',
)
@validate_role(
    role_actions=RoleActions.POST, role_permissions=RolePermissions.EXTRACTS
)
@inject
@error_handler
async def create_extract(
    request: Request,
    file: UploadFile = File(...),
    create_extract_use_case: CreateExtractUseCase = Depends(
        Provide[Container.create_extract_use_case]
    ),
):
    if file.content_type not in ['text/csv', 'application/vnd.ms-excel']:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=ResponseDTO(
                status=StatusEnum.FAIL,
                message='O arquivo deve ser do tipo CSV.',
            ).model_dump(),
        )

    current_user: CurrentUser = request.state.current_user
    response_text: str = await create_extract_use_case.execute(
        file, current_user.email
    )

    return ResponseDTO(
        status=StatusEnum.SUCCESS,
        message=response_text,
    )
