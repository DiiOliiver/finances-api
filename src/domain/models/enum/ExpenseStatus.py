from enum import Enum


class ExpenseStatus(str, Enum):
    OPEN = 'Aberto'
    PAID = 'Pago'
    OVERDUE = 'Atrasado'
    CANCELLED = 'Cancelado'
