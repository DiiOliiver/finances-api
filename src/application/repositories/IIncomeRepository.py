from abc import ABC, abstractmethod
from typing import Optional, TypeVar

from pydantic import BaseModel

from application.dto.PaginationDTO import PaginationDTO
from domain.models.Income import Income

T = TypeVar('T', bound=BaseModel)


class IIncomeRepository(ABC):
    @abstractmethod
    async def add(self, income: T):
        pass

    @abstractmethod
    async def paginate(self, page: int, per_page: int) -> PaginationDTO:
        pass

    @abstractmethod
    async def find_by(self, income_id: str) -> Optional[dict]:
        pass

    @abstractmethod
    async def delete(self, income_id: str):
        pass

    @abstractmethod
    async def update(self, income_id: str, income_data: Income) -> bool:
        pass
