from enum import Enum


class RolePermissions(str, Enum):
    # Generic
    ADMIN = '*'
    AUTH = 'auth'
    EXPENSES = 'expenses'
    EXTRACTS = 'extracts'
    INCOMES = 'incomes'
    NOTEBOOKS = 'notebooks'
    USERS = 'users'
