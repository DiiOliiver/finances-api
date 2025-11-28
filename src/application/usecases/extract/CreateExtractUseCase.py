from http import HTTPStatus
from io import StringIO
from typing import List, Optional

import pandas as pd
from application.dto.ExtractDTO import ExtractDTO
from application.repositories.INotebookRepository import INotebookRepository
from application.utils.NotebookUtils import NotebookUtils
from domain.models.enum.ExpenseStatus import ExpenseStatus
from domain.models.Notebook import Notebook, NotebookExpense
from fastapi import HTTPException, UploadFile


class CreateExtractUseCase:
    def __init__(self, notebook_repository: INotebookRepository, user_id: str):
        self.notebook_repository = notebook_repository
        self.user_id = user_id

    async def execute(self, file: UploadFile):
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
        except Exception as e:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=f'Erro ao ler CSV: {str(e)}',
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
            return {
                'message': 'Listagem!',
                'preview': preview,
                'rows': len(df),
            }
        else:
            expenses: List[NotebookExpense] = [
                NotebookExpense(
                    amount=float(extract['valor']),
                    category=None,
                    description=str(extract['descricao']),
                    status=ExpenseStatus.PAID,
                    created_by=self.user_id,
                )
                for extract in preview
            ]

            notebook = Notebook(
                title=title,
                description='',
                comments=[],
                users=[],
                expenses=expenses,
                created_by=self.user_id,
            )
            await self.notebook_repository.add(notebook)
            return f'Caderneta {notebook.title} foi cadastrada com sucesso.'
