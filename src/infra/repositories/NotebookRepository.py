from math import ceil
from typing import Optional, TypeVar

from pydantic import BaseModel

from application.dto.PaginationDTO import PaginationDTO
from application.repositories.INotebookRepository import INotebookRepository
from domain.models.Notebook import Notebook
from infra.config.settings import Settings
from infra.repositories.BaseRepositoryMongo import BaseRepositoryMongo

T = TypeVar('T', bound=BaseModel)


class NotebookRepository(BaseRepositoryMongo, INotebookRepository):
    def __init__(self, mongodb_connection):
        config = Settings()
        super().__init__(config.DATABASE_NAME, 'notebooks', mongodb_connection)

    async def add(self, notebook: T):
        with self.mongodb_connection.connection() as client:
            db = client[self.database]
            db[self.collection].insert_one(notebook.model_dump(by_alias=True))

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
            data = [Notebook(**doc).model_dump() for doc in data_cursor]

            return PaginationDTO(
                page=page,
                page_size=per_page,
                total_items=total_items,
                total_pages=total_pages,
                data=data,
            )

    async def find_by(self, notebook_id: str) -> Optional[dict]:
        with self.mongodb_connection.connection() as client:
            db = client[self.database]
            data = db[self.collection].find_one({'_id': notebook_id})
            return data if data else None

    async def update(self, notebook_id: str, notebook_data: T):
        with self.mongodb_connection.connection() as client:
            db = client[self.database]

            result = db[self.collection].update_one(
                {'_id': notebook_id}, {'$set': notebook_data}
            )

            return result.modified_count > 0

    async def delete(self, notebook_id: str) -> bool:
        with self.mongodb_connection.connection() as client:
            db = client[self.database]

            notebook_deleted = db[self.collection].delete_one({
                '_id': notebook_id
            })

            return notebook_deleted.deleted_count > 0
