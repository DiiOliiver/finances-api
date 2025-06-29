from math import ceil
from typing import Optional, TypeVar

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, EmailStr

from application.dto.PaginationDTO import PaginationDTO
from application.dto.UserDTO import UserResponseDTO
from application.repositories.IUserRepository import IUserRepository
from domain.models.User import User
from infra.config.settings import Settings
from infra.repositories.BaseRepositoryMongo import BaseRepositoryMongo

T = TypeVar('T', bound=BaseModel)


class UserRepository(BaseRepositoryMongo, IUserRepository):
    def __init__(self, mongodb_connection):
        config = Settings()
        super().__init__(config.DATABASE_NAME, 'users', mongodb_connection)

    async def add(self, user: T):
        with self.mongodb_connection.connection() as client:
            db = client[self.database]
            db[self.collection].insert_one(user.model_dump(by_alias=True))

    async def get_by_email(self, email: EmailStr) -> T:
        with self.mongodb_connection.connection() as client:
            db = client[self.database]
            collection = db[self.collection]
            data = collection.find_one({'email': email})

            return User(**data) if data else None

    async def paginate(self, page: int, per_page: int) -> PaginationDTO:
        offset = (page - 1) * per_page

        paginated_pipeline = [
            {'$sort': {'_id': 1}},
            {'$skip': offset},
            {'$limit': per_page},
        ]

        count_pipeline = [{'$count': 'total'}]

        with self.mongodb_connection.connection() as client:
            db = client[self.database]
            collection = db[self.collection]

            count_cursor = collection.aggregate(count_pipeline)
            count_result = list(count_cursor)
            total_items = count_result[0]['total'] if count_result else 0
            total_pages = ceil(total_items / per_page) if per_page else 1

            data_cursor = collection.aggregate(paginated_pipeline)
            data = [User(**doc).model_dump() for doc in data_cursor]

            return PaginationDTO(
                page=page,
                page_size=per_page,
                total_items=total_items,
                total_pages=total_pages,
                data=data,
            )

    async def find_by(self, user_id: str, model: T) -> Optional[T]:
        with self.mongodb_connection.connection() as client:
            db = client[self.database]
            data = db[self.collection].find_one({'_id': user_id})
            if data:
                user_data = User(**data).model_dump()
                return model(**user_data) if user_data else None
            return None

    async def update(self, user_id: str, user_data: T) -> T | None:
        with self.mongodb_connection.connection() as client:
            db = client[self.database]

            entity_copy = jsonable_encoder(user_data)

            result = db[self.collection].update_one(
                {'_id': user_id}, {'$set': entity_copy}
            )

            if result.modified_count == 0:
                raise Exception(
                    f'Usuário {user_id} não encontrado ou não foi alterado.'
                )

            data = db[self.collection].find_one({'_id': user_id})
            return UserResponseDTO(**data) if data else None

    async def delete(self, user_id: str) -> bool:
        with self.mongodb_connection.connection() as client:
            db = client[self.database]

            user_deleted = db[self.collection].delete_one({'_id': user_id})

            return user_deleted.deleted_count > 0
