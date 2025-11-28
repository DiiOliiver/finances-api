from application.gateway.IUserGateway import IUserGateway
from application.services.UserService import UserService
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
from application.usecases.extract.CreateExtractUseCase import (
    CreateExtractUseCase,
)
from application.usecases.income.CreateIncomeUseCase import CreateIncomeUseCase
from application.usecases.income.DeleteIncomeUseCase import DeleteIncomeUseCase
from application.usecases.income.FindByIncomeUseCase import FindByIncomeUseCase
from application.usecases.income.ListAllIncomeUseCase import (
    ListAllIncomeUseCase,
)
from application.usecases.income.UpdateIncomeUseCase import UpdateIncomeUseCase
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
from application.usecases.user.CreateUserUseCase import CreateUserUseCase
from application.usecases.user.DeleteUserUseCase import DeleteUserUseCase
from application.usecases.user.FindByUserUseCase import FindByUserUseCase
from application.usecases.user.ListAllUserUseCase import ListAllUserUseCase
from application.usecases.user.UpdateUserUseCase import UpdateUserUseCase
from dependency_injector import containers, providers
from infra.config.settings import Settings
from infra.database.MongoDBConection import MongoDBConnection
from infra.repositories.ExpenseRepository import ExpenseRepository
from infra.repositories.IncomeRepository import IncomeRepository
from infra.repositories.NotebookRepository import NotebookRepository
from infra.repositories.UserRepository import UserRepository


class Container(containers.DeclarativeContainer):
    config = Settings()

    wiring_config = containers.WiringConfiguration(
        modules=[
            'infra.router.endpoint.users',
            'infra.router.endpoint.incomes',
            'infra.router.endpoint.notebooks',
            'infra.router.endpoint.expenses',
            'infra.router.endpoint.extracts',
        ]
    )

    # db connection Mongo
    connection_db_mongo = providers.Singleton(
        MongoDBConnection, uri=config.DATABASE_URL
    )

    # Gateway
    user_gateway = providers.Factory(IUserGateway)

    # Repositório mongo database
    user_repository = providers.Factory(
        UserRepository, mongodb_connection=connection_db_mongo
    )

    income_repository = providers.Factory(
        IncomeRepository, mongodb_connection=connection_db_mongo
    )

    notebook_repository = providers.Factory(
        NotebookRepository, mongodb_connection=connection_db_mongo
    )

    expense_repository = providers.Factory(
        ExpenseRepository, mongodb_connection=connection_db_mongo
    )

    # Service
    user_service = providers.Factory(
        UserService, user_repository=user_repository
    )

    # Usecase: users
    create_user_use_case = providers.Factory(
        CreateUserUseCase,
        user_service=user_service,
        user_gateway=user_gateway,
        user_repository=user_repository,
    )

    list_user_use_case = providers.Factory(
        ListAllUserUseCase, user_repository=user_repository
    )

    find_by_user_use_case = providers.Factory(
        FindByUserUseCase, user_repository=user_repository
    )

    update_user_use_case = providers.Factory(
        UpdateUserUseCase,
        user_service=user_service,
        user_repository=user_repository,
    )

    delete_user_use_case = providers.Factory(
        DeleteUserUseCase,
        user_repository=user_repository,
    )

    # Usecase: incomes
    create_income_use_case = providers.Factory(
        CreateIncomeUseCase,
        income_repository=income_repository,
    )

    list_income_use_case = providers.Factory(
        ListAllIncomeUseCase,
        income_repository=income_repository,
        user_repository=user_repository,
    )

    find_by_income_use_case = providers.Factory(
        FindByIncomeUseCase,
        income_repository=income_repository,
        user_repository=user_repository,
    )

    update_income_use_case = providers.Factory(
        UpdateIncomeUseCase,
        income_repository=income_repository,
    )

    delete_income_use_case = providers.Factory(
        DeleteIncomeUseCase,
        income_repository=income_repository,
    )

    # Usecase: notebook
    create_notebook_use_case = providers.Factory(
        CreateNotebookUseCase,
        notebook_repository=notebook_repository,
        user_id=config.USER_ID,
    )

    list_notebook_use_case = providers.Factory(
        ListAllNotebookUseCase,
        notebook_repository=notebook_repository,
        user_repository=user_repository,
    )

    find_by_notebook_use_case = providers.Factory(
        FindByNotebookUseCase,
        notebook_repository=notebook_repository,
        user_repository=user_repository,
    )

    update_notebook_use_case = providers.Factory(
        UpdateNotebookUseCase,
        notebook_repository=notebook_repository,
    )

    delete_notebook_use_case = providers.Factory(
        DeleteNotebookUseCase,
        notebook_repository=notebook_repository,
    )

    # Usecase: notebook
    create_expense_use_case = providers.Factory(
        CreateExpenseUseCase,
        expense_repository=expense_repository,
        user_id=config.USER_ID,
    )

    list_expense_use_case = providers.Factory(
        ListAllExpenseUseCase,
        expense_repository=expense_repository,
    )

    find_by_expense_use_case = providers.Factory(
        FindByExpenseUseCase,
        expense_repository=expense_repository,
    )

    update_expense_use_case = providers.Factory(
        UpdateExpenseUseCase,
        expense_repository=expense_repository,
    )

    delete_expense_use_case = providers.Factory(
        DeleteExpenseUseCase,
        expense_repository=expense_repository,
    )

    # Usecase: extract
    create_extract_use_case = providers.Factory(
        CreateExtractUseCase,
        notebook_repository=notebook_repository,
        user_id=config.USER_ID,
    )
