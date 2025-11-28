from application.dto.IncomeDTO import IncomeResponseDTO
from application.dto.ResponseDTO import ResponseDTO, StatusEnum
from application.repositories.IIncomeRepository import IIncomeRepository
from application.repositories.IUserRepository import IUserRepository
from domain.models.Income import Income
from domain.models.User import User
from fastapi import HTTPException
from starlette.status import (
    HTTP_404_NOT_FOUND,
)


class FindByIncomeUseCase:
    def __init__(
        self,
        income_repository: IIncomeRepository,
        user_repository: IUserRepository,
    ):
        self.income_repository = income_repository
        self.user_repository = user_repository

    async def execute(self, income_id: str) -> IncomeResponseDTO:
        income_data = await self.income_repository.find_by(income_id)
        if not income_data:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND,
                detail=ResponseDTO(
                    status=StatusEnum.FAIL,
                    message='A renda informada não existe.',
                ).model_dump(),
            )

        user_data = await self.user_repository.find_by(income_data['user_id'])
        if not user_data:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND,
                detail=ResponseDTO(
                    status=StatusEnum.FAIL,
                    message='Não há usuário relacionado a renda informada.',
                ).model_dump(),
            )

        user_dto = User(**user_data).model_dump()
        income_model = Income(**income_data).model_dump()
        income_model['user'] = user_dto
        income_model.pop('user_id', None)

        return IncomeResponseDTO(**income_model)
