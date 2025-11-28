from datetime import datetime


class NotebookUtils:
    @staticmethod
    def generate_title_date(date: str) -> str:
        meses = {
            1: 'Janeiro',
            2: 'Fevereiro',
            3: 'Março',
            4: 'Abril',
            5: 'Maio',
            6: 'Junho',
            7: 'Julho',
            8: 'Agosto',
            9: 'Setembro',
            10: 'Outubro',
            11: 'Novembro',
            12: 'Dezembro',
        }
        data_obj = datetime.strptime(date, '%d/%m/%Y')
        return f'{meses[data_obj.month]} de {data_obj.year}'
