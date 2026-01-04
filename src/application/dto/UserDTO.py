from pydantic import BaseModel, EmailStr


class CreateUserDTO(BaseModel):
    name: str
    password: str
    email: EmailStr


class UpdateUserDTO(CreateUserDTO):
    status: bool


class UserResponseDTO(BaseModel):
    id: str
    name: str
    email: EmailStr
    status: bool
