from abc import ABC, abstractmethod
from typing import Optional, TypeVar

from application.dto.PaginationDTO import PaginationDTO
from domain.models import Expense
from pydantic import BaseModel

T = TypeVar('T', bound=BaseModel)


class IExpenseRepository(ABC):
    @abstractmethod
    async def add(self, expense: T):
        pass

    @abstractmethod
    async def paginate(self, page: int, per_page: int) -> PaginationDTO:
        pass

    @abstractmethod
    async def find_by(self, expense_id: str) -> Optional[dict]:
        pass

    @abstractmethod
    async def delete(self, expense_id: str):
        pass

    @abstractmethod
    async def update(self, expense_id: str, expense_data: Expense) -> bool:
        pass
