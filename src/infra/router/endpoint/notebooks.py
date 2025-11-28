from application.dto.NotebookDTO import CreateNotebookDTO, UpdateNotebookDTO
from application.dto.PaginationDTO import PaginationDTO
from application.dto.ResponseDTO import ResponseDTO, StatusEnum
from application.usecases.notebook.CreateNotebookUseCase import (
    CreateNotebookUseCase,
)
from application.usecases.notebook.DeleteNotebookUseCase import (
    DeleteNotebookUseCase,
)
from application.usecases.notebook.FindByNotebookUseCase import (
    FindByNotebookUseCase,
)
from application.usecases.notebook.ListAllNotebookUseCase import (
    ListAllNotebookUseCase,
)
from application.usecases.notebook.UpdateNotebookUseCase import (
    UpdateNotebookUseCase,
)
from application.utils.error_handler import error_handler
from dependency_injector.wiring import Provide, inject
from fastapi import (
    APIRouter,
    Depends,
    Request,
)
from infra.di.Container import Container
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
)

router = APIRouter(prefix='/notebooks', tags=['Notebook'])


@router.post('', status_code=HTTP_201_CREATED, summary='Cadastro de caderneta')
@inject
@error_handler
async def create_notebook(
    request: Request,
    data: CreateNotebookDTO,
    create_notebook_use_case: CreateNotebookUseCase = Depends(
        Provide[Container.create_notebook_use_case]
    ),
) -> ResponseDTO:
    message_response = await create_notebook_use_case.execute(data)
    return ResponseDTO(
        status=StatusEnum.SUCCESS,
        message=message_response,
    )


@router.get(
    '', status_code=HTTP_200_OK, summary='Lista paginável de cadernetas'
)
@inject
@error_handler
async def read_notebooks(
    request: Request,
    page: int = 1,
    per_page: int = 10,
    list_notebook_use_case: ListAllNotebookUseCase = Depends(
        Provide[Container.list_notebook_use_case]
    ),
) -> ResponseDTO:
    pagination: PaginationDTO = await list_notebook_use_case.execute(
        page, per_page
    )
    return ResponseDTO(status=StatusEnum.SUCCESS, data=pagination.dict())


@router.get(
    '/{notebook_id}', status_code=HTTP_200_OK, summary='Consulta caderneta'
)
@inject
@error_handler
async def read_notebook(
    request: Request,
    notebook_id: str,
    find_by_notebook_use_case: FindByNotebookUseCase = Depends(
        Provide[Container.find_by_notebook_use_case]
    ),
) -> ResponseDTO:
    notebook = await find_by_notebook_use_case.execute(notebook_id)
    return ResponseDTO(status=StatusEnum.SUCCESS, data=notebook.dict())


@router.put(
    '/{notebook_id}', status_code=HTTP_200_OK, summary='Atualizar caderneta'
)
@inject
@error_handler
async def update_notebook(
    request: Request,
    notebook_id: str,
    data: UpdateNotebookDTO,
    update_notebook_use_case: UpdateNotebookUseCase = Depends(
        Provide[Container.update_notebook_use_case]
    ),
) -> ResponseDTO:
    message_response = await update_notebook_use_case.execute(
        notebook_id, data
    )
    return ResponseDTO(
        status=StatusEnum.SUCCESS,
        message=message_response,
    )


@router.delete(
    '/{notebook_id}', status_code=HTTP_200_OK, summary='Remover caderneta'
)
@inject
@error_handler
async def delete_notebook(
    request: Request,
    notebook_id: str,
    delete_notebook_use_case: DeleteNotebookUseCase = Depends(
        Provide[Container.delete_notebook_use_case]
    ),
) -> ResponseDTO:
    message_response = await delete_notebook_use_case.execute(notebook_id)
    return ResponseDTO(
        status=StatusEnum.SUCCESS,
        message=message_response,
    )
