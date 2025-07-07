from abc import ABC, abstractmethod
from typing import Optional, TypeVar

from pydantic import BaseModel

from application.dto.PaginationDTO import PaginationDTO
from domain.models.Notebook import Notebook

T = TypeVar('T', bound=BaseModel)


class INotebookRepository(ABC):
    @abstractmethod
    async def add(self, notebook: T):
        pass

    @abstractmethod
    async def paginate(self, page: int, per_page: int) -> PaginationDTO:
        pass

    @abstractmethod
    async def find_by(self, notebook_id: str) -> Optional[dict]:
        pass

    @abstractmethod
    async def delete(self, notebook_id: str):
        pass

    @abstractmethod
    async def update(self, notebook_id: str, notebook_data: Notebook) -> bool:
        pass
