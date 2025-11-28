from application.dto.ExpenseDTO import CreateExpenseDTO, UpdateExpenseDTO
from application.dto.PaginationDTO import PaginationDTO
from application.dto.ResponseDTO import ResponseDTO, StatusEnum
from application.usecases.expense.CreateExpenseUseCase import (
    CreateExpenseUseCase,
)
from application.usecases.expense.DeleteExpenseUseCase import (
    DeleteExpenseUseCase,
)
from application.usecases.expense.FindByExpenseUseCase import (
    FindByExpenseUseCase,
)
from application.usecases.expense.ListAllExpenseUseCase import (
    ListAllExpenseUseCase,
)
from application.usecases.expense.UpdateExpenseUseCase import (
    UpdateExpenseUseCase,
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

router = APIRouter(prefix='/expenses', tags=['Expenses'])


@router.post(
    '', status_code=HTTP_201_CREATED, summary='Cadastro de despesa fixa'
)
@inject
@error_handler
async def create_expense(
    request: Request,
    data: CreateExpenseDTO,
    create_expense_use_case: CreateExpenseUseCase = Depends(
        Provide[Container.create_expense_use_case]
    ),
) -> ResponseDTO:
    message_response = await create_expense_use_case.execute(data)
    return ResponseDTO(
        status=StatusEnum.SUCCESS,
        message=message_response,
    )


@router.get(
    '', status_code=HTTP_200_OK, summary='Lista paginável de despesas fixas'
)
@inject
@error_handler
async def read_expenses(
    request: Request,
    page: int = 1,
    per_page: int = 10,
    list_expense_use_case: ListAllExpenseUseCase = Depends(
        Provide[Container.list_expense_use_case]
    ),
) -> ResponseDTO:
    pagination: PaginationDTO = await list_expense_use_case.execute(
        page, per_page
    )
    return ResponseDTO(status=StatusEnum.SUCCESS, data=pagination.dict())


@router.get(
    '/{expense_id}', status_code=HTTP_200_OK, summary='Consulta despesa fixa'
)
@inject
@error_handler
async def read_expense(
    request: Request,
    expense_id: str,
    find_by_expense_use_case: FindByExpenseUseCase = Depends(
        Provide[Container.find_by_expense_use_case]
    ),
) -> ResponseDTO:
    expense = await find_by_expense_use_case.execute(expense_id)
    return ResponseDTO(status=StatusEnum.SUCCESS, data=expense.dict())


@router.put(
    '/{expense_id}', status_code=HTTP_200_OK, summary='Atualizar despesa fixa'
)
@inject
@error_handler
async def update_expense(
    request: Request,
    expense_id: str,
    data: UpdateExpenseDTO,
    update_expense_use_case: UpdateExpenseUseCase = Depends(
        Provide[Container.update_expense_use_case]
    ),
) -> ResponseDTO:
    message_response = await update_expense_use_case.execute(expense_id, data)
    return ResponseDTO(
        status=StatusEnum.SUCCESS,
        message=message_response,
    )


@router.delete(
    '/{expense_id}', status_code=HTTP_200_OK, summary='Remover caderneta'
)
@inject
@error_handler
async def delete_expense(
    request: Request,
    expense_id: str,
    delete_expense_use_case: DeleteExpenseUseCase = Depends(
        Provide[Container.delete_expense_use_case]
    ),
) -> ResponseDTO:
    message_response = await delete_expense_use_case.execute(expense_id)
    return ResponseDTO(
        status=StatusEnum.SUCCESS,
        message=message_response,
    )
