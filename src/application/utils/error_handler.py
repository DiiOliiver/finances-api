import logging
from functools import wraps

from application.dto.ResponseDTO import ResponseDTO, StatusEnum
from fastapi import HTTPException
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

logger = logging.getLogger('Error Handler')


def error_handler(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            logger.error(f'Erro inesperado: {exc}')
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ResponseDTO(
                status=StatusEnum.ERROR,
                message='Ocorreu um erro interno no servidor.',
            ).model_dump(),
        )

    return wrapper
