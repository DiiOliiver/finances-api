from abc import ABC, abstractmethod
from typing import Optional, Type, TypeVar

T = TypeVar('T')


class IBaseRepository(ABC):
    @abstractmethod
    async def get(self, id: str, model: Type[T]) -> Optional[T]:
        """
        Used to fetch a record by its id.
        :param model: Discriminate the type of return
        :param id: MongoDB hash id, model
        :return: [T] - entity
        """
        raise NotImplementedError

    @abstractmethod
    def create(self, entity: T) -> T:
        """
        Create a new person.
        """
        raise NotImplementedError('Implement IBaseRepository')

    @abstractmethod
    def delete(self, id: int) -> None:
        """
        Delete a new person.
        """
        raise NotImplementedError('Implement IBaseRepository')

    @abstractmethod
    def update(self, id: str, entity: T) -> T:
        """
        Update a new person.
        """
        raise NotImplementedError('Implement IBaseRepository')
