from dependency_injector import containers, providers

from application.gateway.IUserGateway import IUserGateway
from application.services.UserService import UserService
from application.usecases.income.CreateIncomeUseCase import CreateIncomeUseCase
from application.usecases.income.DeleteIncomeUseCase import DeleteIncomeUseCase
from application.usecases.income.FindByIncomeUseCase import FindByIncomeUseCase
from application.usecases.income.ListAllIncomeUseCase import (
    ListAllIncomeUseCase,
)
from application.usecases.income.UpdateIncomeUseCase import UpdateIncomeUseCase
from application.usecases.user.CreateUserUseCase import CreateUserUseCase
from application.usecases.user.DeleteUserUseCase import DeleteUserUseCase
from application.usecases.user.FindByUserUseCase import FindByUserUseCase
from application.usecases.user.ListAllUserUseCase import ListAllUserUseCase
from application.usecases.user.UpdateUserUseCase import UpdateUserUseCase
from infra.config.settings import Settings
from infra.database.MongoDBConection import MongoDBConnection
from infra.repositories.IncomeRepository import IncomeRepository
from infra.repositories.UserRepository import UserRepository


class Container(containers.DeclarativeContainer):
    config = Settings()

    wiring_config = containers.WiringConfiguration(
        modules=[
            'infra.router.endpoint.users',
            'infra.router.endpoint.incomes',
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
