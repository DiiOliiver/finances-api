from pydantic import BaseModel


class ExtractDTO(BaseModel):
    date: str
    value: float
    identifier: str
    description: str
