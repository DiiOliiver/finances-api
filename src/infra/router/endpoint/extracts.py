from http import HTTPStatus

from application.usecases.extract import CreateExtractUseCase
from application.utils.error_handler import error_handler
from dependency_injector.wiring import Provide, inject
from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    Request,
    UploadFile,
)
from infra.di.Container import Container
from starlette.status import (
    HTTP_201_CREATED,
)

router = APIRouter(prefix='/extracts', tags=['Extracts'])


@router.post(
    '/upload-csv',
    status_code=HTTP_201_CREATED,
    summary='Upload de extrato bancário',
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
            detail='O arquivo deve ser um CSV.',
        )

    return await create_extract_use_case.execute(file)
