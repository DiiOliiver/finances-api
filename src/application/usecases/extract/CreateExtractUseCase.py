import logging
from http import HTTPStatus
from io import StringIO
from typing import List, Optional

import pandas as pd
from application.dto.ExtractDTO import ExtractDTO
from application.dto.ResponseDTO import ResponseDTO, StatusEnum
from application.repositories.INotebookRepository import INotebookRepository
from application.repositories.IUserRepository import IUserRepository
from application.utils.NotebookUtils import NotebookUtils
from domain.models.enum.ExpenseStatus import ExpenseStatus
from domain.models.Notebook import Notebook, NotebookExpense
from domain.models.User import User
from fastapi import HTTPException, UploadFile
from pydantic import EmailStr

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CreateExtractUseCase:
    def __init__(
        self,
        notebook_repository: INotebookRepository,
        user_repository: IUserRepository,
    ):
        self.notebook_repository = notebook_repository
        self.user_repository = user_repository

    async def execute(self, file: UploadFile, email: EmailStr):
        contents = await file.read()

        try:
            text = contents.decode('utf-8')

            df = pd.read_csv(StringIO(text))

            df.columns = [col.lower().strip() for col in df.columns]
            df = df.rename(
                columns={
                    'data': 'data',
                    'valor': 'valor',
                    'identificador': 'identificador',
                    'descrição': 'descricao',
                }
            )

            preview = df[
                ['data', 'valor', 'identificador', 'descricao']
            ].to_dict(orient='records')
        except Exception as exc:
            logging.error(f'Erro ao ler CSV: {exc}')
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=ResponseDTO(
                    status=StatusEnum.FAIL, message='Erro ao ler CSV'
                ).model_dump(),
            )

        extract_data = preview[1]
        extract_dto = ExtractDTO(
            date=extract_data.get('data', ''),
            value=extract_data.get('valor', 0.0),
            identifier=extract_data.get('identificador', ''),
            description=extract_data.get('descricao', ''),
        )

        title = NotebookUtils.generate_title_date(extract_dto.date)
        notebook: Optional[Notebook] = await self.notebook_repository.find_by(
            title
        )

        if notebook:
            return HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail=ResponseDTO(
                    status=StatusEnum.FAIL,
                    message=f'Caderneta {title} já existe.',
                ),
            )

        user: User = await self.user_repository.get_by_email(email=email)

        expenses: List[NotebookExpense] = [
            NotebookExpense(
                amount=float(extract['valor']),
                category=None,
                description=str(extract['descricao']),
                status=ExpenseStatus.PAID,
                created_by=user.id,
            )
            for extract in preview
        ]

        notebook = Notebook(
            title=title,
            description=f'Importado de extrato em {file.filename}',
            comments=[],
            users=[],
            expenses=expenses,
            created_by=user.id,
        )
        await self.notebook_repository.add(notebook)
        return f'Caderneta {notebook.title} foi cadastrada com sucesso.'
