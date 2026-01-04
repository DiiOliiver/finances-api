import logging
from functools import wraps
from http import HTTPStatus

from application.dto.ResponseDTO import ResponseDTO, StatusEnum
from fastapi import HTTPException

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


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
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=ResponseDTO(
                status=StatusEnum.ERROR,
                message='Ocorreu um erro interno no servidor.',
            ).model_dump(),
        )

    return wrapper
