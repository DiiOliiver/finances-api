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

from application.dto.IncomeDTO import CreateIncomeDTO, UpdateIncomeDTO
from application.dto.PaginationDTO import PaginationDTO
from application.dto.ResponseDTO import ResponseDTO, StatusEnum
from application.usecases.income.CreateIncomeUseCase import CreateIncomeUseCase
from application.usecases.income.DeleteIncomeUseCase import DeleteIncomeUseCase
from application.usecases.income.FindByIncomeUseCase import FindByIncomeUseCase
from application.usecases.income.ListAllIncomeUseCase import (
    ListAllIncomeUseCase,
)
from application.usecases.income.UpdateIncomeUseCase import UpdateIncomeUseCase
from application.utils.error_handler import error_handler
from infra.di.Container import Container

router = APIRouter(prefix='/incomes', tags=['Incomes'])


@router.post('', status_code=HTTP_201_CREATED, summary='Cadastro de renda')
@inject
@error_handler
async def create_income(
    request: Request,
    data: CreateIncomeDTO,
    create_income_use_case: CreateIncomeUseCase = Depends(
        Provide[Container.create_income_use_case]
    ),
) -> ResponseDTO:
    message_response = await create_income_use_case.execute(data)
    return ResponseDTO(
        status=StatusEnum.SUCCESS,
        message=message_response,
    )


@router.get('', status_code=HTTP_200_OK, summary='Lista paginável de rendas')
@inject
@error_handler
async def read_incomes(
    request: Request,
    page: int = 1,
    per_page: int = 10,
    list_income_use_case: ListAllIncomeUseCase = Depends(
        Provide[Container.list_income_use_case]
    ),
) -> ResponseDTO:
    pagination: PaginationDTO = await list_income_use_case.execute(
        page, per_page
    )
    return ResponseDTO(status=StatusEnum.SUCCESS, data=pagination.dict())


@router.get('/{income_id}', status_code=HTTP_200_OK, summary='Consulta renda')
@inject
@error_handler
async def read_income(
    request: Request,
    income_id: str,
    find_by_income_use_case: FindByIncomeUseCase = Depends(
        Provide[Container.find_by_income_use_case]
    ),
):
    income = await find_by_income_use_case.execute(income_id)
    return ResponseDTO(status=StatusEnum.SUCCESS, data=income.dict())


@router.put('/{income_id}', status_code=HTTP_200_OK, summary='Atualizar renda')
@inject
@error_handler
async def update_income(
    request: Request,
    income_id: str,
    data: UpdateIncomeDTO,
    update_income_use_case: UpdateIncomeUseCase = Depends(
        Provide[Container.update_income_use_case]
    ),
) -> ResponseDTO:
    message_response = await update_income_use_case.execute(income_id, data)
    return ResponseDTO(
        status=StatusEnum.SUCCESS,
        message=message_response,
    )


@router.delete(
    '/{income_id}', status_code=HTTP_200_OK, summary='Remover renda'
)
@inject
@error_handler
async def delete_income(
    request: Request,
    income_id: str,
    delete_income_use_case: DeleteIncomeUseCase = Depends(
        Provide[Container.delete_income_use_case]
    ),
) -> ResponseDTO:
    message_response = await delete_income_use_case.execute(income_id)
    return ResponseDTO(
        status=StatusEnum.SUCCESS,
        message=message_response,
    )
