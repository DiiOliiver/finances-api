from dependency_injector import containers, providers

from application.gateway.IUserGateway import IUserGateway
from application.services.UserService import UserService
from application.usecases.user.CreateUserUseCase import CreateUserUseCase
from application.usecases.user.DeleteUserUseCase import DeleteUserUseCase
from application.usecases.user.FindByUserUseCase import FindByUserUseCase
from application.usecases.user.ListAllUserUseCase import ListAllUserUseCase
from application.usecases.user.UpdateUserUseCase import UpdateUserUseCase
from infra.config.settings import Settings
from infra.database.MongoDBConection import MongoDBConnection
from infra.repositories.UserRepository import UserRepository


class Container(containers.DeclarativeContainer):
    config = Settings()

    wiring_config = containers.WiringConfiguration(
        modules=[
            'infra.router.endpoint.users',
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

    # Service
    user_service = providers.Factory(
        UserService, user_repository=user_repository
    )

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
