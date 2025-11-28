from contextlib import AbstractContextManager
from typing import Callable, Optional, Type, TypeVar

from application.repositories.IBaseRepository import IBaseRepository
from pydantic import BaseModel
from pymongo import MongoClient

T = TypeVar('T', bound=BaseModel)


class BaseRepositoryMongo(IBaseRepository):
    def __init__(
        self,
        database: str,
        collection: str,
        mongodb_connection: Callable[..., AbstractContextManager[MongoClient]],
    ):
        self.database = database
        self.collection = collection
        self.mongodb_connection = mongodb_connection

    async def get(self, id: str, model: Type[T]) -> Optional[T]:
        with self.mongodb_connection.connection() as client:
            db = client[self.database]
            data = db[self.collection].find_one({'_id': id})

            return await self.__convert_dict_to_object(data, model)

    async def create(self, model: T) -> T:
        with self.mongodb_connection.connection() as client:
            db = client[self.database]
            db[self.collection].insert_one(model.model_dump(by_alias=True))
            return model

    async def delete(self, id: str):
        with self.mongodb_connection.connection() as client:
            db = client[self.database]

            user_deleted = db[self.collection].delete_one({'_id': id})

            return user_deleted.deleted_count

    async def update(self, id: str, entity: T) -> T:
        update_dict = await self.__convert_object_to_dict(entity)
        if update_dict is None:
            return None

        with self.mongodb_connection.connection() as client:
            db = client[self.database]
            data = db[self.collection].update_one(
                {'_id': id}, {'$set': update_dict}, upsert=False
            )
            return data

    @staticmethod
    async def __convert_object_to_dict(model: T) -> dict | None:
        if model is None:
            return None
        return model.model_dump()

    @staticmethod
    async def __convert_dict_to_object(
        dict_model: dict, model: Type[T]
    ) -> T | None:
        if dict_model is None:
            return None
        return model(**dict_model)
