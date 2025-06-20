from datetime import datetime
from typing import Optional
from uuid import uuid4

from pydantic import BaseModel, EmailStr, Field


class User(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()), alias='_id')
    name: str = Field(
        ..., min_length=1, max_length=100, description='Nome do usuário'
    )
    email: EmailStr = Field(
        ..., min_length=5, max_length=100, description='Nome do usuário'
    )
    status: bool = Field(
        True, description='Status do usuário. Ativo(true) Inativo(false)'
    )
    created_at: datetime = Field(
        default_factory=datetime.now,
        description='Data da criação do registro.',
    )
    updated_at: Optional[datetime] = Field(
        None, description='Data da atualização do registro.'
    )

    class Config:
        populate_by_name = True

    @classmethod
    def create(cls, name: str, email: str) -> 'User':
        return cls(
            name=name,
            email=email,
            status=True,
            created_at=datetime.utcnow(),
            updated_at=None,
        )
