from http import HTTPStatus
from typing import Any, Dict, Optional


class ServiceErrorDTO(Exception):
    def __init__(
        self,
        message: str,
        status_code: HTTPStatus,
        details: Optional[Dict[str, Any]] = None,
        validated_roles: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, Any]] = None,
        *args: object,
    ) -> None:
        self.message = message
        self.status_code = status_code
        self.details = details
        self.validated_roles = validated_roles
        self.headers = headers
        super().__init__(*args)

    def __str__(self) -> str:
        base_message = f'{self.status_code}: {self.message}'
        if self.details:
            details_message = f' Details: {self.details}'
            base_message += details_message
        if self.validated_roles:
            roles_message = f' Validated Roles: {self.validated_roles}'
            base_message += roles_message
        return base_message
