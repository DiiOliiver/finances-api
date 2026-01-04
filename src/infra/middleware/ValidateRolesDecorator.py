from functools import wraps
from http import HTTPStatus

import jwt
from application.dto.ServiceErrorDTO import ServiceErrorDTO
from domain.CurrentUser import CurrentUser
from domain.models.enum import RolePermissions
from domain.models.enum.RoleActions import RoleActions
from domain.models.enum.RoleModules import RoleModules


def validate_role(
    role_actions: RoleActions,
    role_permissions: RolePermissions,
    role_module: RoleModules = RoleModules.GERAL,
):
    def decorator(handler):
        @wraps(handler)
        async def wrapper(*args, **kwargs):
            request = kwargs.get('request')
            authorization_header = request.headers.get('Authorization')

            if not authorization_header or not authorization_header.startswith(
                'Bearer '
            ):
                raise ServiceErrorDTO(
                    status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                    message='Cabeçalho de autorização ausente ou inválido.',
                )
            token = authorization_header.split('Bearer ')[1]
            try:
                payload = jwt.decode(
                    token, options={'verify_signature': False}
                )
            except jwt.ExpiredSignatureError:
                raise ServiceErrorDTO(
                    status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                    message='O token expirou.',
                )
            except jwt.InvalidTokenError:
                raise ServiceErrorDTO(
                    status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                    message='Token inválido',
                )

            request.state.current_user = CurrentUser(
                user_pk=payload.get('sub'),
                name=payload.get('name'),
                email=payload.get('email'),
                roles=payload.get('roles'),
            )

            return await handler(*args, **kwargs)

        return wrapper

    return decorator
