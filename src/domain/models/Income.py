from datetime import datetime
from typing import Optional
from uuid import uuid4

from bson import ObjectId
from pydantic import BaseModel, Field


class Income(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()), alias='_id')
    user_id: str = Field(
        ..., min_length=1, max_length=100, description='Id do usuário'
    )
    amount: float = Field(..., description='Valor da renda')
    income_day: str = Field(..., description='Dia da renda')
    category: Optional[str] = Field(None, description='Categoria')
    description: Optional[str] = Field(None, description='Descrição')
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
