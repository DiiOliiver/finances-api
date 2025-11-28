import re
from http import HTTPStatus

from application.dto.ServiceErrorDTO import ServiceErrorDTO
from fastapi import Request
from fastapi.exceptions import RequestValidationError, ResponseValidationError
from fastapi.responses import JSONResponse
from jwt.exceptions import DecodeError
from pydantic import ValidationError


class ExceptionMiddleware:
    @staticmethod
    async def exception_handler(
        request: Request, ex: Exception
    ) -> JSONResponse:
        status_code = 500
        headers = None
        formatted_errors = [
            {
                'name': 500,
                'errors': 'Error not Mapped',
            }
        ]

        if isinstance(ex, ServiceErrorDTO):
            formatted_errors = [
                {
                    'name': ex.status_code,
                    'errors': f'{ex.status_code}: {ex.message}',
                }
            ]
            status_code = ex.status_code
            headers = ex.headers

        elif isinstance(ex, RequestValidationError):
            formatted_errors = [
                {
                    'name': ' -> '.join(str(p) for p in err['loc'])
                    if err['loc']
                    else 'general',
                    'errors': [err['msg']],
                }
                for err in ex.errors()
            ]
            status_code = 422

        elif isinstance(ex, ValidationError):
            if ex.title == 'DataSendForSerialNumbersFile':
                formatted_errors = [
                    {
                        'name': 422,
                        'errors': 'Preencha todos os campos obrigatórios no arquivo Serial Numbers para serviços e envie o arquivo novamente.',
                    }
                ]
            else:
                formatted_errors = [
                    {
                        'name': ' -> '.join(str(p) for p in err['loc'])
                        if err['loc']
                        else 'general',
                        'errors': [err['msg']],
                    }
                    for err in ex.errors()
                ]
            status_code = 422

        elif isinstance(ex, DecodeError):
            formatted_errors = [
                {
                    'name': 500,
                    'errors': 'Verifique o Bearer',
                    'validated_roles': 'No roles',
                }
            ]
            status_code = 500

        elif isinstance(ex, AttributeError):
            formatted_errors = [
                {
                    'name': 422,
                    'errors': f'Atributo com erro: {str(ex)}',
                }
            ]
            status_code = 422

        elif isinstance(ex, ResponseValidationError):
            error_inputs = re.findall(r"'input':\s*({.*?})", str(ex))
            input_error = (
                error_inputs[0] if error_inputs else 'No input error found'
            )
            formatted_errors = [
                {
                    'name': 401,
                    'errors': f'Atributo com erro: {input_error}',
                }
            ]
            status_code = 401

        elif isinstance(ex, Exception):
            formatted_errors = [
                {
                    'name': 400,
                    'errors': str(ex),
                }
            ]
            status_code = HTTPStatus.BAD_REQUEST

        return JSONResponse(
            status_code=status_code,
            content=formatted_errors,
            headers=headers,
        )
