from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar('T')


class PaginationDTO(BaseModel, Generic[T]):
    """
    DTO para os responses de listas paginadas.
    """

    page: int
    page_size: int
    total_items: int
    total_pages: int
    data: list[T]
