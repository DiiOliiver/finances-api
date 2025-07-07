from enum import Enum


class ExpenseStatus(str, Enum):
    OPEN = 'open'
    PAID = 'paid'
    OVERDUE = 'overdue'
    CANCELLED = 'cancelled'
