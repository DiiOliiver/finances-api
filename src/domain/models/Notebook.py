from datetime import datetime
from typing import List, Optional
from uuid import uuid4

from bson import ObjectId
from pydantic import BaseModel, Field

from domain.models import Expense


class NotebookComment(BaseModel):
    message: str = Field(..., description='Mensagem')
    user_id: str = Field(..., description='Id do usuário')
    created_at: datetime = Field(
        default_factory=datetime.now,
        description='Data da criação do registro.',
    )
    updated_at: Optional[datetime] = Field(
        None, description='Data da atualização do registro.'
    )


class Notebook(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()), alias='_id')
    title: str = Field(..., description='Título da caderneta')
    description: Optional[str] = Field(
        None, description='Descrição da caderneta'
    )
    users: Optional[List[str]] = Field(
        None, description='Usuários com acesso a caderneta'
    )
    comments: Optional[List[NotebookComment]] = Field(
        None, description='Comentário de usuários'
    )
    expenses: Optional[List[Expense]] = Field(
        None, description='Despesa de usuários'
    )
    created_by: str = Field(None, description='Usuário que criou o registro')
    created_at: datetime = Field(
        default_factory=datetime.now,
        description='Data da criação do registro.',
    )
    updated_at: Optional[datetime] = Field(
        None, description='Data da atualização do registro.'
    )

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        allow_population_by_field_name = True
