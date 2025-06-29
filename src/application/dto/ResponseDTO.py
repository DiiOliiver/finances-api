from enum import Enum
from typing import Optional

from pydantic import BaseModel


class StatusEnum(str, Enum):
    SUCCESS = 'success'
    FAIL = 'fail'
    ERROR = 'error'


class ResponseDTO(BaseModel):
    status: StatusEnum = StatusEnum.ERROR
    message: Optional[str] = None
    data: Optional[dict] = None
