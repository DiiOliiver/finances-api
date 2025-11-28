from abc import ABC, abstractmethod
from typing import Optional, TypeVar

from application.dto.PaginationDTO import PaginationDTO
from domain.models.User import User
from pydantic import BaseModel, EmailStr

T = TypeVar('T', bound=BaseModel)


class IUserRepository(ABC):
    @abstractmethod
    async def add(self, user: T):
        pass

    @abstractmethod
    async def get_by_email(self, email: EmailStr) -> T:
        pass

    @abstractmethod
    async def paginate(self, page: int, per_page: int) -> PaginationDTO:
        pass

    @abstractmethod
    async def find_by(self, user_id: str) -> Optional[dict]:
        pass

    @abstractmethod
    async def find_many_by_ids(self, user_ids: list[str]) -> list[dict]:
        pass

    @abstractmethod
    async def delete(self, user_id: str):
        pass

    @abstractmethod
    async def update(self, user_id: str, user_data: User) -> bool:
        pass
